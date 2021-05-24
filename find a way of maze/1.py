# BFS
from queue import Queue
import queue
import heapq
import math

Code = range(1, 1, 19)


def Act(code, StringList):
    after = StringList.strip("[]")
    after = after.split(", ")
    for i in range(0, len(after)):
        after[i] = int(after[i])
    if code == 1:
        after[0] = after[0] + 1
    elif code == 2:
        after[0] = after[0] - 1
    elif code == 3:
        after[1] = after[1] + 1
    elif code == 4:
        after[1] = after[1] - 1
    elif code == 5:
        after[2] = after[2] + 1
    elif code == 6:
        after[2] = after[2] - 1
    elif code == 7:
        after[0] = after[0] + 1
        after[1] = after[1] + 1
    elif code == 8:
        after[0] = after[0] + 1
        after[1] = after[1] - 1
    elif code == 9:
        after[0] = after[0] - 1
        after[1] = after[1] + 1
    elif code == 10:
        after[0] = after[0] - 1
        after[1] = after[1] - 1
    elif code == 11:
        after[0] = after[0] + 1
        after[2] = after[2] + 1
    elif code == 12:
        after[0] = after[0] + 1
        after[2] = after[2] - 1
    elif code == 13:
        after[0] = after[0] - 1
        after[2] = after[2] + 1
    elif code == 14:
        after[0] = after[0] - 1
        after[2] = after[2] - 1
    elif code == 15:
        after[1] = after[1] + 1
        after[2] = after[2] + 1
    elif code == 16:
        after[1] = after[1] + 1
        after[2] = after[2] - 1
    elif code == 17:
        after[1] = after[1] - 1
        after[2] = after[2] + 1
    elif code == 18:
        after[1] = after[1] - 1
        after[2] = after[2] - 1
    return after


def loadInput(fileName):
    fileIn = open(fileName, "r")
    data = {}
    i = 1
    for line in fileIn:
        line = line.strip("\n")
        parameter = line.split(" ")
        if i == 1:
            Type = parameter
        elif i == 2:
            for item in range(0, len(parameter)):
                parameter[item] = int(parameter[item])
            dimension = parameter
        elif i == 3:
            for item in range(0, len(parameter)):
                parameter[item] = int(parameter[item])
            s = parameter
        elif i == 4:
            for item in range(0, len(parameter)):
                parameter[item] = int(parameter[item])
            v = parameter
        elif i == 5:
            for item in range(0, len(parameter)):
                parameter[item] = int(parameter[item])
            totalNum = parameter
        else:
            for item in range(0, len(parameter)):
                parameter[item] = int(parameter[item])
            if parameter[0] < dimension[0] and parameter[1] < dimension[1] and parameter[2] < dimension[2]:
                data[str(parameter[0:3])] = parameter[3:]
        i = i + 1
        # for key in data.keys():
        # print(str(key) + ": " + str(data[key]))
    return Type, dimension, s, v, totalNum, data


def ConfigureBFS(Data):
    maze = {}
    for grid in Data.keys():
        # GridString = str(grid[0:3])
        maze.setdefault(grid, [])
        i = 0
        while i < len(Data[grid]):
            current = str(Act(Data[grid][i], grid))
            # print(str(grid) + ": " + str(current))
            if current in Data.keys():
                maze[grid].append(current)
            i = i + 1
    # for key in maze.keys():
    # print(str(key) + ": " + str(maze[key]))
    return maze


def ConfigureUCS(Data):
    maze = {}
    for grid in Data.keys():
        # GridString = str(grid[0:3])
        maze.setdefault(grid, [])
        i = 0
        while i < len(Data[grid]):
            current = str(Act(Data[grid][i], grid))
            # print(str(grid) + ": " + str(current))
            if 0 < Data[grid][i] < 7:
                cost = 10
            else:
                cost = 14
            if current in Data.keys():
                maze[grid].append((cost, current))
            i = i + 1
    # for key in maze.keys():
    # print(str(key) + ": " + str(maze[key]))
    return maze


def PathCost(Node1, node2):
    cost = Node1[0] + node2[0]
    return (cost, node2[1]), node2[0]


def PathCostForAStar(Node1, node2):
    cost = Node1[1] + node2[0]
    return (cost, node2[1]), node2[0]


def HeuristicCost(node2, end):
    coordinate = node2[1].strip("'[]'")
    coordinate = coordinate.split(", ")
    for item in range(0, len(coordinate)):
        coordinate[item] = int(coordinate[item])
    square = abs((end[0] - coordinate[0]) ^ 2 + (end[1] - coordinate[1]) ^ 2 + (end[2] - coordinate[2]) ^ 2)
    sqrt = math.sqrt(square)
    hCost = 10 * sqrt
    return hCost


# print(len(Data['grid']))
# for key in maze.values():
# print(key[0][1])


def main():
    Type, Dimension, start, end, TotalNum, Data = loadInput("input.txt")
    if Type == ['BFS']:
        Maze = ConfigureBFS(Data)
        visited = {}
        level = {}
        parent = {}
        cost = 0
        step = 0
        bfs = []
        q = Queue()
        for node in Maze.keys():
            visited[node] = False
            parent[node] = None
            level[node] = -1
        s = str(start)
        visited[s] = True
        level[s] = 0
        if s not in Maze.keys() or str(end) not in Maze.keys():
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
            exit()
        q.put(s)
        while not q.empty():
            u = q.get()
            bfs.append(u)
            for v in Maze[u]:
                if not visited[v]:
                    visited[v] = True
                    parent[v] = u
                    level[v] = level[v] + 1
                    q.put(v)
        v = str(end)
        path = []
        while v is not None:
            path.append(v)
            v = parent[v]
            step = step + 1
            if v != s:
                cost = cost + 1
        path.reverse()
        if path[0] != str(start):
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
            exit()
        fileOut = open("output.txt", "w")
        print(cost, file=fileOut)
        print(step, file=fileOut)
        for words in path:
            if words == s:
                print(words.strip("'[]'").replace(',', '') + " " + "0", file=fileOut)
            else:
                print(words.strip("'[]'").replace(',', '') + " " + "1", file=fileOut)
        fileOut.close()
    elif Type == ['UCS']:
        Maze = ConfigureUCS(Data)
        path = []
        step = 1
        visited = {}
        level = {}
        parent = {}
        Closed = {}
        Child = {}
        Open = []
        s = str(start)
        parent[s] = (0, 0)
        v = str(end)
        if s not in Maze.keys() or str(end) not in Maze.keys():
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
            exit()
        visited[s] = True
        level[s] = 0
        heapq.heappush(Open, (0, s))
        move = heapq.heappop(Open)
        while move[1] != v:
            Closed[move[1]] = move[0]
            for element in Open:
                Child[element[1]] = element[0]
            for node in Maze[move[1]]:
                Node, edge = PathCost(move, node)
                if Node[1] in Child.keys() and Node[0] < Child[Node[1]]:
                    Open.remove((Child[Node[1]], Node[1]))
                    heapq.heappush(Open, Node)
                    parent[Node[1]] = (edge, move[1])
                elif Node[1] in Closed.keys() and Node[0] < Closed[Node[1]]:
                    moveback = Closed.pop(Node[1])
                    heapq.heappush(Open, (moveback, Node[1]))
                    parent[Node[1]] = (edge, move[1])
                elif Node[1] not in Child.keys() and Node[1] not in Closed.keys():
                    heapq.heappush(Open, Node)
                    parent[Node[1]] = (edge, move[1])
            move = heapq.heappop(Open)
            Closed[move[1]] = move[0]
        cost = move[0]
        # print(parent)
        # print(Closed)
        # print(cost)
        path.append((parent[v][0], v))
        # print(parent[v])
        while parent[v] != (0, 0):
            v = parent[v][1]
            step = step + 1
            # print(v)
            path.append((parent[v][0], v))
        path.reverse()
        if path[0][1] != str(start):
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
            exit()
        fileOut = open("output.txt", "w")
        print(cost, file=fileOut)
        print(step, file=fileOut)
        for words in path:
            print(words[1].strip("'[]'").replace(',', '') + " " + str(words[0]), file=fileOut)
        fileOut.close()
    elif Type == ['A*']:
        Maze = ConfigureUCS(Data)
        path = []
        step = 1
        cost = 0
        visited = {}
        level = {}
        parent = {}
        Closed = {}
        Child = {}
        g = {}
        Open = []
        s = str(start)
        parent[s] = (0, 0, 0)
        v = str(end)
        if s not in Maze.keys() or str(end) not in Maze.keys():
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
            exit()
        visited[s] = True
        level[s] = 0
        heapq.heappush(Open, (0, 0, s))
        move = heapq.heappop(Open)
        while move[2] != v:
            Closed[move[2]] = move[0:2]
            for element in Open:
                Child[element[2]] = element[0:2]
            for node in Maze[move[2]]:
                Node, edge = PathCostForAStar(move, node)
                f = Node[0] + HeuristicCost(node, end)
                fNode = (f, Node[0], Node[1])
                #print(fNode)
                if fNode[2] in Child.keys() and fNode[0] < Child[fNode[2]][0]:
                    Open.remove((Child[fNode[2]][0], Child[fNode[2]][1], fNode[2]))
                    heapq.heappush(Open, fNode)
                    parent[fNode[2]] = (edge, move[2])
                elif fNode[2] in Closed.keys() and fNode[0] < Closed[fNode[2]][0]:
                    moveback = Closed.pop(fNode[2])
                    heapq.heappush(Open, (moveback[0], moveback[1], fNode[2]))
                    parent[fNode[2]] = (edge, move[2])
                elif fNode[2] not in Child.keys() and fNode[2] not in Closed.keys():
                    heapq.heappush(Open, fNode)
                    parent[fNode[2]] = (edge, move[2])
            move = heapq.heappop(Open)
            Closed[move[2]] = move[0:2]
        #print(Child)
        #print(parent)
        #print(Closed)
        # print(cost)
        path.append((parent[v][0], v))
        # print(parent[v])
        while parent[v] != (0, 0, 0):
            cost = cost + parent[v][0]
            v = parent[v][1]
            step = step + 1
            path.append((parent[v][0], v))
        path.reverse()
        if path[0][1] != str(start):
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
            exit()
        fileOut = open("output.txt", "w")
        print(cost, file=fileOut)
        print(step, file=fileOut)
        for words in path:
            print(words[1].strip("'[]'").replace(',', '') + " " + str(words[0]), file=fileOut)
        fileOut.close()


main()
