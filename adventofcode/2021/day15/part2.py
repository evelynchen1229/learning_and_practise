from construction import constructor
import math
import numpy as np
from bigmap import fullmaze 

def maze_map(position_list):
    maze_position = [position[::-1] for position in position_list]
    return maze_position

def adjacents(current_node, max_rows, max_cols):
    row = current_node[0]
    col = current_node[1]

    above = [row - 1, col]
    below = [row + 1, col]
    left = [row, col - 1]
    right = [row, col + 1]
    
    adjacent_nodes = [above, below, left, right]

    legal_adjacents = [adjacent for adjacent in adjacent_nodes if 0 <= adjacent[0] < max_rows and 0 <= adjacent[1] < max_cols]

    return legal_adjacents

#challenge = constructor('input.txt')
challenge = fullmaze('input.txt')
maze = maze_map(challenge['position'])
cost = challenge['values']
maze_shape = np.shape(cost)
max_rows = maze_shape[0]
max_cols = maze_shape[1]

initial_t_dist = np.zeros((maze_shape))+math.inf
initial_t_dist[0,0] = 0

def dijkstra():
    current_node = [0,0]
    unvisited_nodes = maze
    t_dist = initial_t_dist

    destination = max(maze)

    while True:
        print(current_node)

        if len(unvisited_nodes) == 0:
            raise Exception("Did not get to destination")

        if current_node == destination:
            total_cost = t_dist[current_node[0],current_node[1]]
            return total_cost

        unvisited_nodes.remove(current_node)

        neighbour_nodes = adjacents(current_node, max_rows, max_cols)
        unvisited_neighbours = [node for node in neighbour_nodes if node in unvisited_nodes]

        for node in unvisited_neighbours: 
            tentative_dist = t_dist[current_node[0],current_node[1]] + cost[node[0]][node[1]] 
            if tentative_dist < t_dist[node[0],node[1]]:
                t_dist[node[0],node[1]] = tentative_dist
        
        unvisited_cost = [t_dist[node[0],node[1]] for node in unvisited_nodes]
        index = unvisited_cost.index(min(unvisited_cost))
        current_node = unvisited_nodes[index]

test = dijkstra()
print(test)
