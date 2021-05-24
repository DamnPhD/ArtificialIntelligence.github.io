# CS561 HW2 by Jun
# last modify on Oct 10th
import random
from copy import deepcopy
import heapq


def readInboard(n=5, path="input.txt"):
    with open(path, 'r') as inputfile:
        lines = inputfile.readlines()
        player_type = int(lines[0])
        previous_board = [[int(x) for x in line.rstrip('\n')] for line in lines[1:n + 1]]
        current_board = [[int(x) for x in line.rstrip('\n')] for line in lines[n + 1: 2 * n + 1]]

    return player_type, previous_board, current_board


def writeOutput(my_move, path="output.txt"):
    # my move is the result after the strategy, type: list
    # when chose PASS, use my_move = [-1, -1]
    # if my_move == [-1, -1]:
    if my_move == "PASS" or my_move == (-1, -1):
        with open(path, 'w') as outputfile:
            outputfile.write("PASS")
    else:
        result_output = ""
        result_output += str(my_move[0]) + ',' + str(my_move[1])
        with open(path, 'w') as outputfile:
            outputfile.write(result_output)


class GO_GAME:
    def __init__(self, n):
        self.size = n
        self.player_type = 0
        self.previous_board = []
        self.current_board = []
        self.captured = []  # find captured stone position (i,j) caused by opponent's move
        self.opponent_type = 0
        self.opponent_pass = False  # find out if opponent pass the move
        self.opponent_move_position = []  # opponents move, if pass [-1 -1]

    def set_board(self, player_type, previous_board, current_board):
        self.player_type = player_type
        self.previous_board = previous_board
        self.current_board = current_board

        """
        (i,j) = (row, column), (0,0) is defined as top left, (0,4) is defined as top right
        """
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == player_type and current_board[i][j] != player_type:
                    self.captured.append((i, j))

    def opponent_move(self):

        previous_board = self.previous_board
        current_board = self.current_board
        player_type = self.player_type
        self.opponent_type = 3 - player_type
        # self.set_board(player_type, previous_board, current_board)
        self.opponent_pass = True
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] != current_board[i][j]:
                    self.opponent_pass = False

        if not self.opponent_pass:
            for i in range(self.size):
                for j in range(self.size):
                    if previous_board[i][j] == 0 and current_board[i][j] == self.opponent_type:
                        self.opponent_move_position = [i, j]
        else:
            self.opponent_move_position = [-1, -1]

    def find_neighbor(self, i, j):

        current_board = self.current_board
        neighbors = []

        if i > 0: neighbors.append((i - 1, j))
        if i < (self.size - 1): neighbors.append((i + 1, j))
        if j > 0: neighbors.append((i, j - 1))
        if j < (self.size - 1): neighbors.append((i, j + 1))
        return neighbors

    def find_neighbor_ally(self, i, j):

        board = self.current_board
        neighbor_ally = []
        neighbors = self.find_neighbor(i, j)
        # print(neighbors)
        for neighbor in neighbors:
            if board[neighbor[0]][neighbor[1]] == board[i][j]:
                neighbor_ally.append(neighbor)
        return neighbor_ally

    def find_all_ally(self, i, j):
        queue = [(i, j)]
        all_ally_list = []
        while queue:
            element = queue.pop()
            all_ally_list.append(element)
            neighbor_allies = self.find_neighbor_ally(element[0], element[1])
            for ally in neighbor_allies:
                if ally not in queue and ally not in all_ally_list:
                    queue.append(ally)
        return all_ally_list

    def find_liberty(self, i, j):
        current_board = self.current_board
        all_ally = self.find_all_ally(i, j)
        for element in all_ally:
            neighbor_positions = self.find_neighbor(element[0], element[1])
            for position in neighbor_positions:
                if current_board[position[0]][position[1]] == 0:
                    return True
        return False

    def find_noliberty_stone(self, piece_type):
        board = self.current_board
        noliberty_stone = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type and not self.find_liberty(i, j):
                    noliberty_stone.append((i, j))

        return noliberty_stone

    def remove_noliberty_stone(self, piece_type):
        board = self.current_board
        noliberty_stone = self.find_noliberty_stone(piece_type)
        if not noliberty_stone:
            self.current_board = board
        else:
            for stone in noliberty_stone:
                board[stone[0]][stone[1]] = 0

        self.update_board(board)

    def check_board(self, board1, board2):

        if len(board1) != len(board2):
            return False
        else:
            for i in range(len(board1)):
                for j in range(len(board2)):
                    if board1[i][j] != board2[i][j]:
                        return False
            return True

    def copy_board(self):
        return deepcopy(self)

    def update_board(self, new_board):
        self.current_board = new_board

    def valid_place_check(self, i, j, piece_type):
        board = self.current_board
        if board[i][j] != 0:
            return False

        test_game = self.copy_board()
        test_gameboard = test_game.current_board
        test_gameboard[i][j] = piece_type
        test_game.update_board(test_gameboard)

        if test_game.find_liberty(i, j):
            return True

        test_game.remove_noliberty_stone(3 - piece_type)
        if not test_game.find_liberty(i, j):
            return False
        elif self.check_board(self.previous_board, test_game.current_board):
            return False

        return True

    def print_check(self):
        print(self.current_board)
        print(self.opponent_pass)
        print(self.opponent_move_position)
        print(self.find_all_ally(2, 2))

    def count_piece(self, piece_type):
        board = self.current_board
        num_cnt = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] == piece_type:
                    num_cnt += 1
        return num_cnt

    def count_allstone_onboard(self):
        board = self.current_board
        num_all = 0
        for i in range(self.size):
            for j in range(self.size):
                if board[i][j] != 0:
                    num_all += 1
        return num_all

    def eval_score(self):
        board_eval = self.current_board
        black_num = 0  # black is max player
        white_num = 0  # white is min player
        for i in range(len(board_eval)):
            for j in range(len(board_eval)):
                if board_eval[i][j] == 1:
                    black_num += 1
                elif board_eval[i][j] == 2:
                    white_num += 1
        eval_value = black_num - white_num
        return eval_value


def eval_fun(board):
    black_num = 0  # black is max player
    white_num = 0  # white is min player
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == 1:
                black_num += 1
            elif board[i][j] == 2:
                white_num += 1
    eval_value = black_num - white_num

    return eval_value


"""
function need to realize except the strategy of chess placement 
1. place_unoccupied
2. valid_place_check KO rule, suicide rule 
3. valid_place_check special case: need liberty until remove captured stones
3. suicide_rule check by liberty 
4. komi
5. if other player pass 
6. partial area, count numbers
[done]7. write output after the strategy in format 

Questions:
1. Pre and post board already remove die_piece?
2. How to avoid the large area suicide 

Strategy player train by myself:
1. can use .json or .txt helper files to store Q-value table 
2. Minimax, a-b pruning
3.reinforcement learning
4. Q-learning (might use the host to train the Q-learning agent)
5. each move less than 10 sec
"""


# verify code, need modify
class RandomPlayer():
    def __init__(self):
        self.type = 'random'

    def get_input(self, game, piece_type):
        '''
        Get one input.

        :param go: Go instance.
        :param piece_type: 1('X') or 2('O').
        :return: (row, column) coordinate of input.
        '''
        possible_placements = []
        for i in range(game.size):
            for j in range(game.size):
                if game.valid_place_check(i, j, piece_type):
                    possible_placements.append((i, j))

        if not possible_placements:
            return "PASS"
        else:
            return random.choice(possible_placements)


class MiniMaxPlayer():
    def __init__(self):
        self.type = 'minimax'
        self.action = (-1, -1)
        self.value = 0
        self.test_board = []

    def minimax_move(self, game, depth, alpha, beta, piece_type, move_num):

        if move_num < 8:
            possible_placements = []
            for i in range(1, game.size - 1):
                for j in range(1, game.size - 1):
                    if game.valid_place_check(i, j, piece_type):
                        possible_placements.append((i, j))
            return 0, random.choice(possible_placements)


        else:
            '''
            possible_placements = []
            for i in range(game.size):
                for j in range(game.size):
                    if game.valid_place_check(i, j, piece_type):
                        possible_placements.append((i, j))
                        '''

            ordered_position = [(2, 2), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0), (2, 0),
                                (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3),
                                (4, 2), (4, 1), (4, 0)]
            possible_placements = []
            for i, j in ordered_position:
                if game.valid_place_check(i, j, piece_type):
                    possible_placements.append((i, j))

            if not possible_placements:
                eval_value = game.eval_score()
                return (eval_value, self.action)

            if depth == 0:
                return (game.eval_score(), self.action)

            if piece_type == 1:
                maxEval = float('-inf')
                eval_act = []
                for position in possible_placements:
                    original_board = deepcopy(game.current_board)
                    test_board = deepcopy(original_board)
                    test_board[position[0]][position[1]] = piece_type
                    game.update_board(test_board)
                    game.remove_noliberty_stone(3 - piece_type)
                    eval_value, self.action = self.minimax_move(game, depth - 1, alpha, beta, 2, 8)
                    # heapq.heappush(eval_act, (eval_value, position))
                    game.update_board(original_board)

                    if eval_value > maxEval:
                        maxEval = eval_value
                        move = position
                    # maxEval = max(maxEval, eval_value)
                    alpha = max(alpha, eval_value)
                    if beta < alpha:
                        break
                # heapq._heapify_max(eval_act)
                # return heapq._heappop_max(eval_act)
                return maxEval, move



            else:
                minEval = float('inf')
                eval_act = []
                for position in possible_placements:

                    original_board = deepcopy(game.current_board)
                    test_board = deepcopy(original_board)
                    test_board[position[0]][position[1]] = piece_type
                    game.update_board(test_board)

                    game.remove_noliberty_stone(3 - piece_type)
                    eval_value, self.action = self.minimax_move(game, depth - 1, alpha, beta, 1, 8)
                    # heapq.heappush(eval_act, (eval_value, position)) # may use dic not heapq
                    game.update_board(original_board)

                    if eval_value < minEval:
                        minEval = eval_value
                        move = position
                    # minEval = min(minEval, eval_value)
                    beta = min(beta, eval_value)
                    if beta < alpha:
                        break
                # heapq.heapify(eval_act)
                # return heapq.heappop(eval_act)
                return minEval, move


if __name__ == "__main__":
    board_size = 5
    player_type, previous_board, current_board = readInboard(board_size, "input.txt")
    game = GO_GAME(board_size)
    game.set_board(player_type, previous_board, current_board)
    player = MiniMaxPlayer()
    min_inf = float('-inf')
    max_inf = float('inf')
    stone_num = game.count_allstone_onboard()
    score, action = player.minimax_move(game, 3, min_inf, max_inf, player_type, stone_num)
    # print(action)

    writeOutput(action, "output.txt")
