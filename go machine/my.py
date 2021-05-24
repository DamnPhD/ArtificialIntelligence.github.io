from copy import deepcopy


ordered_position = [(1, 1), (1, 3), (3, 3), (3, 1), (1, 2), (2, 3), (3, 2), (2, 1), (2, 2), (0, 0), (0, 1), (0, 2),
                    (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (4, 0), (3, 0), (2, 0),
                            (1, 0)]

"""ordered_position = [(2, 2), (2, 1), (1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (3, 2), (3, 1), (3, 0), (2, 0),
                            (1, 0), (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3),
                            (4, 2), (4, 1), (4, 0)]"""

class GO_GAME:
    def __init__(self, n):
        self.size = n
        self.player_type = 0
        self.previous_board = []
        self.current_board = []
        self.captured = []  # find captured stone position (i,j) caused by opponent's move
        self.opponent_type = 0
        self.opponent_pass = False
        self.opponent_move_position = []

    def setBoard(self, player_type, previous_board, current_board):
        self.player_type = player_type
        self.previous_board = previous_board
        self.current_board = current_board

        """
        if one chess is captured by the opponent.
        """
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] == player_type and current_board[i][j] != player_type:
                    self.captured.append((i, j))

    def opponentMove(self):

        previous_board = self.previous_board
        current_board = self.current_board
        player_type = self.player_type
        self.opponent_type = 3 - player_type
        for i in range(self.size):
            for j in range(self.size):
                if previous_board[i][j] != current_board[i][j] and current_board[i][j] == self.opponent_type:
                    self.opponent_pass = False
                    self.opponent_move_position = [i, j]
                elif previous_board[i][j] == current_board[i][j]:
                    self.opponent_pass = True
                    self.opponent_move_position = [-1, -1]


    def findNeighbor(self, i, j):

        neighbors = []

        if i > 0:
            neighbors.append((i - 1, j))
        if i < (self.size - 1):
            neighbors.append((i + 1, j))
        if j > 0:
            neighbors.append((i, j - 1))
        if j < (self.size - 1):
            neighbors.append((i, j + 1))
        return neighbors

    def findNeighborAlly(self, i, j):

        board = self.current_board
        neighborAlly = []
        neighbors = self.findNeighbor(i, j)
        # print(neighbors)
        for neighbor in neighbors:
            if board[neighbor[0]][neighbor[1]] == board[i][j]:
                neighborAlly.append(neighbor)
        return neighborAlly

    def findConnectedAlly(self, i, j):
        queue = [(i, j)]
        allAlly = []
        while queue:
            element = queue.pop()
            allAlly.append(element)
            neighborAlly = self.findNeighborAlly(element[0], element[1])
            for ally in neighborAlly:
                if ally not in queue and ally not in allAlly:
                    queue.append(ally)
        return allAlly

    def findLiberty(self, i, j):
        current_board = self.current_board
        ConnectedAlly = self.findConnectedAlly(i, j)
        for element in ConnectedAlly:
            neighbor = self.findNeighbor(element[0], element[1])
            for position in neighbor:
                if current_board[position[0]][position[1]] == 0:
                    return True
        return False

    def findNolibertyStone(self, piece_type):
        board = self.current_board
        NolibertyStone = []
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == piece_type and not self.findLiberty(i, j):
                    NolibertyStone.append((i, j))

        return NolibertyStone

    def removeNolibertyStone(self, piece_type):
        board = self.current_board
        NolibertyStone = self.findNolibertyStone(piece_type)
        if not NolibertyStone:
            self.current_board = board
        else:
            for stone in NolibertyStone:
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
        testGame = self.copy_board()
        testGameboard = testGame.current_board
        testGameboard[i][j] = piece_type
        testGame.update_board(testGameboard)
        if testGame.findLiberty(i, j):
            return True
        testGame.removeNolibertyStone(3 - piece_type)
        if not testGame.findLiberty(i, j):
            return False
        elif self.check_board(self.previous_board, testGame.current_board):
            return False
        return True

    def print_check(self):
        print(self.current_board)
        print(self.opponent_pass)
        print(self.opponent_move_position)
        print(self.findConnectedAlly(2, 2))

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


    def compare_board(self, board1, board2):
        for i in range(self.size):
            for j in range(self.size):
                if board1[i][j] != board2[i][j]:
                    return False
        return True


    def game_end(self, piece_type, action="MOVE"):
        '''
        Check if the game should end.

        :param piece_type: 1('X') or 2('O').
        :param action: "MOVE" or "PASS".
        :return: boolean indicating whether the game should end.
        '''

        # Case 1: max move reached
        if self.n_move >= self.max_move:
            return True
        # Case 2: two players all pass the move.
        if self.compare_board(self.previous_board, self.board) and action == "PASS":
            return True
        return False


def readInboard(boardSize):
    fileIn = open("input.txt", "r")
    previous_board = []
    current_board = []
    i = 0
    for line in fileIn:
        line = line.strip("\n")
        if i == 0:
            player_type = int(line[0])
        elif 0 < i < boardSize + 1:
            string = [int(x) for x in line]
            previous_board.append(string)
        else:
            string = [int(x) for x in line]
            current_board.append(string)
        i = i + 1
    """print(player_type)
    print(previous_board)
    print(current_board)"""
    return player_type, previous_board, current_board


def writeOutput(my_move):
    if my_move == "PASS" or my_move == (-1, -1):
        fileOut = open("output.txt", "w")
        print("PASS", file=fileOut)
    else:
        output = ""
        output = output + str(my_move[0]) + ',' + str(my_move[1])
        fileOut = open("output.txt", "w")
        print(output, file=fileOut)


class MiniMaxPlayer:
    def __init__(self):
        self.type = 'minimax'
        self.action = (-1, -1)
        self.value = 0
        self.test_board = []
        self.positionInOrder = ordered_position

    def minimax_move(self, game, depth, alpha, beta, piece_type):
        # first, check the availability of the possible positions
        possible_placements = []
        for i, j in self.positionInOrder:
            if game.valid_place_check(i, j, piece_type):
                possible_placements.append((i, j))

        if not possible_placements:
            eval_value = game.eval_score()
            return eval_value, self.action
        # when finish the depth research, return the evaluation value
        if depth == 0:
            return game.eval_score(), self.action

        if piece_type == 1:
            maxEval = float('-inf')
            for position in possible_placements:
                original_board = deepcopy(game.current_board)
                test_board = deepcopy(original_board)
                test_board[position[0]][position[1]] = piece_type
                game.update_board(test_board)
                game.removeNolibertyStone(3 - piece_type)
                eval_value, self.action = self.minimax_move(game, depth - 1, alpha, beta, 2)
                game.update_board(original_board)
                # update the alpha
                if eval_value > maxEval:
                    maxEval = eval_value
                    move = position
                alpha = max(alpha, eval_value)
                if beta < alpha:
                    break
            return maxEval, move
        else:
            minEval = float('inf')
            for position in possible_placements:
                original_board = deepcopy(game.current_board)
                test_board = deepcopy(original_board)
                test_board[position[0]][position[1]] = piece_type
                game.update_board(test_board)
                game.removeNolibertyStone(3 - piece_type)
                eval_value, self.action = self.minimax_move(game, depth - 1, alpha, beta, 1)
                game.update_board(original_board)
                # update the
                if eval_value < minEval:
                    minEval = eval_value
                    move = position
                beta = min(beta, eval_value)
                if beta < alpha:
                    break
            return minEval, move


if __name__ == "__main__":
    board_size = 5
    player_type, previous_board, current_board = readInboard(board_size)
    game = GO_GAME(board_size)
    game.setBoard(player_type, previous_board, current_board)
    player = MiniMaxPlayer()
    # set the min and max to a infinite value
    min_inf = float('-inf')
    max_inf = float('inf')
    stone_num = game.count_allstone_onboard()
    if stone_num < 16:
        # when the move number is small, use a less-depth min-max function to reduce the processing time
        score, action = player.minimax_move(game, 2, min_inf, max_inf, player_type)
    else:
        score, action = player.minimax_move(game, 4, min_inf, max_inf, player_type)
    #print(action)

    writeOutput(action)
