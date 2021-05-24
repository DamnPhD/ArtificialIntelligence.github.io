# 2020 Fall CSCI 561 HW1 by Jun
import heapq


input_file = "input6.txt"
output_file = "output_trial6.txt"

#read in data
search_alg = ""
maze_size = []
maze_in = []
maze_out = []
num_grids = 0
arr_grids = []

with open(input_file, 'r') as file:
    search_alg = file.readline().replace('\n', '')
    maze_size = [int(x) for x in next(file).split()]
    maze_in = [int(x) for x in next(file).split()]
    maze_out = [int(x) for x in next(file).split()]
    num_grids = int(next(file))
    for line in file:
        arr_grids.append([int(x) for x in line.split()])
#print(arr_grids)

# operation of the point


def action(in_point, act_num):
    out_point = in_point
    if act_num == 1:
        out_point[0] += 1
    elif act_num == 2:
        out_point[0] -= 1
    elif act_num == 3:
        out_point[1] += 1
    elif act_num == 4:
        out_point[1] -= 1
    elif act_num == 5:
        out_point[2] += 1
    elif act_num == 6:
        out_point[2] -= 1
    elif act_num == 7:
        out_point[0] += 1
        out_point[1] += 1
    elif act_num == 8:
        out_point[0] += 1
        out_point[1] -= 1
    elif act_num == 9:
        out_point[0] -= 1
        out_point[1] += 1
    elif act_num == 10:
        out_point[0] -= 1
        out_point[1] -= 1
    elif act_num == 11:
        out_point[0] += 1
        out_point[2] += 1
    elif act_num == 12:
        out_point[0] += 1
        out_point[2] -= 1
    elif act_num == 13:
        out_point[0] -= 1
        out_point[2] += 1
    elif act_num == 14:
        out_point[0] -= 1
        out_point[2] -= 1
    elif act_num == 15:
        out_point[1] += 1
        out_point[2] += 1
    elif act_num == 16:
        out_point[1] += 1
        out_point[2] -= 1
    elif act_num == 17:
        out_point[1] -= 1
        out_point[2] += 1
    elif act_num == 18:
        out_point[1] -= 1
        out_point[2] -= 1
    return out_point


def graph(num_grids, arr_grids):
    # creat a dictionary to store all the points and their coordinates
    point_dic = {}
    for i in range(num_grids):
        point_dic[str(i)] = arr_grids[i][0:3]

    # creat a dictionary to store the graph
    graph_dic = {}
    for i in range(num_grids):
        value_list = []  # list of connected points
        num_act = len(arr_grids[i]) - 3
        for j in range(num_act):
            output_point = action(arr_grids[i][0:3], arr_grids[i][j + 3])
            for point, value in point_dic.items():
                if value == output_point:
                    value_list.append(str(point))
        graph_dic[str(i)] = value_list

    return graph_dic, point_dic


def graph_ucs(num_grids, arr_grids):
    # creat a dictionary to store all the points and their coordinates
    point_dic = {}
    for i in range(num_grids):
        point_dic[str(i)] = arr_grids[i][0:3]


    # creat a dictionary to store the graph and edge cost
    graph_dic_ucs = {}
    for i in range(num_grids):
        value_list = []
        num_act = len(arr_grids[i])-3
        for j in range(num_act):
            output_point = action(arr_grids[i][0:3], arr_grids[i][j+3])
            if arr_grids[i][j+3] > 6:
                edge_cost = 14;
            else:
                edge_cost = 10;
            for point, value in point_dic.items():
                if value == output_point:
                    value_list.append([str(point), edge_cost])
        graph_dic_ucs[str(i)] = value_list

    return graph_dic_ucs, point_dic


def bfs(maze_size, maze_in, maze_out, graph,point_in):
    num_step = 0
    arr_step = []
    explored = []
    queue = []

    for point, values in point_in.items():
        if values == maze_in:
            start = point
        if values == maze_out:
            goal = point

    queue.append([start])

    if start == goal:
        print("start == goal")

    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            neighbours = graph[node]
            #print(neighbours)
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == goal:
                    return new_path, len(new_path)
            explored.append(node)


def ucs(maze_size, maze_in, maze_out, graph_in, point_in):
    path = []
    explored_nodes =list()
    in_frontier = False
    for point, values in point_in.items():
        if values == maze_in:
            start = point
        if values == maze_out:
            goal = point

    if start == goal:
        return path
    path.append(start)
    path_cost = 0
    frontier = [(path_cost, path)]
    #print(frontier)
    while len(frontier) > 0:
        path_cost_now, path_now = frontier.pop(0)
        #print(path_cost_now)
        #print(path_now)
        current_node = path_now[-1]
        explored_nodes.append(current_node)
        if current_node == goal:
            return path_now, path_cost_now

        neighbours = graph_in[current_node]
        neighbours_list_int = [int(neighbour[0]) for neighbour in neighbours]
        neighbours_list_int.sort(reverse=False)
        neighbours_list_str = [str(neighbour) for neighbour in neighbours_list_int]

        #print(neighbours)
        #print(neighbours_list_str)
        for neighbour in neighbours_list_str:
            path_to_neigbhour = path_now.copy()
            path_to_neigbhour.append(neighbour)

            for node, cost in neighbours:
                if node == neighbour:
                    extra_cost = cost

            neighbour_cost = extra_cost + path_cost_now
            new_element = (neighbour_cost, path_to_neigbhour)
            for i in range(len(frontier)):
                if frontier[i][1][0] == neighbour:
                    in_frontier = True
                    neighbour_index = i
                    neighbour_old_cost = frontier[i][0]
                else:
                    in_frontier = False

            if (neighbour not in explored_nodes) and not in_frontier:
                frontier.append(new_element)
            elif in_frontier:
                if neighbour_old_cost > neighbour_cost:
                    frontier.pop(neighbour_index)
                    frontier.append(new_element)


def output_write(point_in, path, num_step):
    with open(output_file, 'w') as file:
        file.write(str(num_step-1)+'\n')
        file.write(str(num_step) + '\n')
        for i in range(num_step):
            if i == 0:
                for j in range(3):
                    file.write(str(point_in.get(path[i])[j]) + ' ')
                file.write('0'+'\n')
            elif i == num_step-1:
                for j in range(3):
                    file.write(str(point_in.get(path[i])[j]) + ' ')
                file.write('1')
            else:
                for j in range(3):
                    file.write(str(point_in.get(path[i])[j]) + ' ')
                file.write('1' + '\n')


def output_write_ucs(point_in, path, cost, cost_step):
    with open(output_file, 'w') as file:
        file.write(str(cost)+'\n')
        file.write(str(len(path)) + '\n')
        for i in range(len(path)):
            if i == 0:
                for j in range(3):
                    file.write(str(point_in.get(path[i])[j]) + ' ')
                file.write('0'+'\n')
            elif i == len(path)-1:
                for j in range(3):
                    file.write(str(point_in.get(path[i])[j]) + ' ')
                file.write(str(cost_step[-1]))
            else:
                for j in range(3):
                    file.write(str(point_in.get(path[i])[j]) + ' ')
                file.write(str(cost_step[i-1]) + '\n')


if search_alg == "BFS":
    graph_in, point_in = graph(num_grids, arr_grids)
    path, num_step = bfs(maze_size, maze_in, maze_out, graph_in, point_in)
    output_write(point_in, path, num_step)

elif search_alg == "UCS":
    graph_in, point_in = graph_ucs(num_grids, arr_grids)
    path, cost = ucs(maze_size, maze_in, maze_out, graph_in, point_in)
    cost_step = []
    for i in range(len(path)-1):
        neighbours = graph_in[path[i]]
        for node, value in neighbours:
            if path[i+1] == node:
                cost_step.append(value)
    output_write_ucs(point_in, path, cost, cost_step)


elif search_alg == "A*":
    a_star()

