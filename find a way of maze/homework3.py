from queue import Queue
from queue import PriorityQueue
# create function for actions
def actions(move, newGrid, grid):
    if move == "1":
        newGrid[0] = int(grid[0]) + 1
    elif move == "2":
        newGrid[0] = int(grid[0]) - 1
    elif move == "3":
        newGrid[1] = int(grid[1]) + 1
    elif move == "4":
        newGrid[1] = int(grid[1]) - 1
    elif move == "5":
        newGrid[2] = int(grid[2]) + 1
    elif move == "6":
        newGrid[2] = int(grid[2]) - 1
    elif move == "7":
        newGrid[0] = int(grid[0]) + 1
        newGrid[1] = int(grid[1]) + 1
    elif move == "8":
        newGrid[0] = int(grid[0]) + 1
        newGrid[1] = int(grid[1]) - 1
    elif move == "9":
        newGrid[0] = int(grid[0]) - 1
        newGrid[1] = int(grid[1]) + 1
    elif move == "10":
        newGrid[0] = int(grid[0]) - 1
        newGrid[1] = int(grid[1]) - 1
    elif move == "11":
        newGrid[0] = int(grid[0]) + 1
        newGrid[2] = int(grid[2]) + 1
    elif move == "12":
        newGrid[0] = int(grid[0]) + 1
        newGrid[2] = int(grid[2]) - 1
    elif move == "13":
        newGrid[0] = int(grid[0]) - 1
        newGrid[2] = int(grid[2]) + 1
    elif move == "14":
        newGrid[0] = int(grid[0]) - 1
        newGrid[2] = int(grid[2]) - 1
    elif move == "15":
        newGrid[1] = int(grid[1]) + 1
        newGrid[2] = int(grid[2]) + 1
    elif move == "16":
        newGrid[1] = int(grid[1]) + 1
        newGrid[2] = int(grid[2]) - 1
    elif move == "17":
        newGrid[1] = int(grid[1]) - 1
        newGrid[2] = int(grid[2]) + 1
    elif move == "18":
        newGrid[1] = int(grid[1]) - 1
        newGrid[2] = int(grid[2]) - 1
    else:
        fileOut = open("output.txt", "w")
        print("FAIL", file=fileOut)
    newGrid[0] = str(newGrid[0])
    newGrid[1] = str(newGrid[1])
    newGrid[2] = str(newGrid[2])
    return

def graph(gridLocationList, dimensions):
    gridInfo = {}
    for gridLine in gridLocationList:
        gridLine = gridLine.strip().split(" ")
        grid = gridLine[0:3]
        actionsSet = gridLine[3:]
        neighborSet = []
        if int(grid[0]) > int(dimensions[0]) or int(grid[1]) > int(dimensions[1]) or int(grid[2]) > int(dimensions[2]):
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
        for move in actionsSet:
            newGrid = gridLine[0:3]
            actions(move, newGrid, grid)
            newGrid = ",".join(newGrid)
            neighborSet.append(newGrid)
        grid = ",".join(grid)
        gridInfo[grid] = neighborSet
    return gridInfo

def usc_cost(gridLocationList):
    cost = {}
    for gridLine in gridLocationList:
        gridLine = gridLine.strip().split(" ")
        grid = gridLine[0:3]
        grid = ",".join(grid)
        actionsSet = gridLine[3:]
        for move in actionsSet:
            newGrid = gridLine[0:3]
            actions(move, newGrid, gridLine[0:3])
            newGrid = ",".join(newGrid)
            if int(move) > 0 and int(move) < 7:
                cost[grid, newGrid] = 10
            elif int(move) >= 7 and int(move) < 19:
                cost[grid, newGrid] = 14
            newGrid = ",".join(newGrid)
    return cost

def ucs(gridInfo, startGrid, exitGrid, gridLocationList):
    visitedNode = []
    cost = usc_cost(gridLocationList)
    cost[startGrid] = 0
    queue = PriorityQueue()
    queue.put((0, startGrid, [startGrid]))
    if startGrid not in gridInfo.keys():
        fileOut = open("output.txt", "w")
        print("FAIL", file=fileOut)
    while not queue.empty():
        (currentCost, node, path) = queue.get()
        if node not in visitedNode:
            visitedNode.append(node)

            if node == exitGrid:
                fileOut = open("output44.txt", "w")
                print(currentCost, file=fileOut)
                pathList = path
                print(len(pathList), file=fileOut)
                for i in range(len(pathList)):
                    nodeList = pathList[i].split(",")
                    j = 0
                    while j < len(pathList):
                        j = i + 1
                        print(nodeList[0], nodeList[1], nodeList[2], cost[pathList[i], pathList[j]], file=fileOut)
            for i in gridInfo[node]:
                if i not in visitedNode:
                    total_cost = currentCost + cost[node, i]
                    queue.put((total_cost, i, path + [i]))
                else:
                    total_cost = min(total_cost, currentCost + cost[node, i])
                    queue.put((total_cost, i, path + [i]))

                #print(cost['5,1,3', '5,2,3'], file=fileOut)




def bfs(gridInfo, startGrid, exitGrid):
    visitedNode = {}
    cost = {}
    parentNode = {}
    traversal = []
    queue = Queue()

    for gridNode in gridInfo.keys():
        visitedNode[gridNode] = False
        parentNode[gridNode] = None
        cost[gridNode] = -1
    visitedNode[startGrid] = True
    cost[startGrid] = 0
    queue.put(startGrid)

    while not queue.empty():
        u = queue.get()
        traversal.append(u)
        if startGrid not in traversal:
            fileOut = open("output.txt", "w")
            print("FAIL", file=fileOut)
        else:
            for v in gridInfo[u]:
                if not visitedNode[v]:
                    visitedNode[v] = True
                    parentNode[v] = u
                    cost[v] = cost[u] + 1
                    queue.put(v)
    fileOut = open("output.txt", "w")
    print("FAIL", file=fileOut)
    # shortest path of from any node from source node
    path = []
    v = exitGrid
    if v not in traversal:
        fileOut = open("output.txt", "w")
        print("FAIL", file=fileOut)
    else:
        while v is not None:
            path.append(v)
            v = parentNode[v]
        path.reverse()
        fileOut = open("output.txt", "w")
        print(cost[exitGrid], file=fileOut)
        print(cost[exitGrid] + 1, file=fileOut)
        startGridList = startGrid.split(",")
        print(startGridList[0], startGridList[1], startGridList[2], cost[startGrid], file=fileOut)
        for gridNode in path[1:]:
            gridNodeList = gridNode.split(",")
            u = parentNode[gridNode]
            print(gridNodeList[0], gridNodeList[1], gridNodeList[2], cost[gridNode] - cost[u], file=fileOut)
    return



def main():
    # read file
    fileIn = open("input2.txt", "r")
    lines = fileIn.readlines()
    algorithm = lines[0].strip()
    dimensions = lines[1].strip().split(" ")
    gridNum = int(lines[4])
    startGrid = lines[2].strip().split(" ")
    exitGrid = lines[3].strip().split(" ")
    startGrid = ",".join(startGrid)
    exitGrid = ",".join(exitGrid)
    fileIn.close()
    # create a dictionary to get all grid with their own available neighbor grid.
    gridInfo = graph(lines[5:5+gridNum], dimensions)
    # bfs code
    if algorithm == "BFS":
        bfs(gridInfo, startGrid, exitGrid)
    elif algorithm == "UCS":
        print(ucs(gridInfo, startGrid, exitGrid, lines[5:5+gridNum]))
        ucs(gridInfo, startGrid, exitGrid, lines[5:5 + gridNum])
        print(usc_cost(lines[5:5+gridNum]))

main()
