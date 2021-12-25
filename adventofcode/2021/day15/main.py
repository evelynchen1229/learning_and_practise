from construction import constructor
from warnings import warn

challenge = constructor('input.txt')
maze = challenge['position']
cost = challenge['values']
maze_length = len(cost[0])
maze_height = len(cost)
start = min(maze)
end = max(maze)

diagonal = False

class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = cost[self.position[1]][self.position[0]] 
        self.h = 0 #(end[0] - self.position[0]) ** 2 + (end[1] - self.position[1]) ** 2
        self.f = self.g + self.h 

    def __eq__(self, other):
        return self.position == other.position

    def __repr__(self):
        return f"{self.position}"
    
    def __lt__(self, other):
        return self.f < other.f

    def __gt__(self, other):
        return self.f > other.f


def adjacents(current_node):
    x = current_node.position[0]
    y = current_node.position[1]

    above = [x, y-1]
    below = [x, y+1]
    left = [x-1, y]
    right = [x+1, y]
    diagonal_upperleft = [x-1, y-1]
    diagonal_upperright = [x+1, y-1]
    diagonal_lowerleft = [x-1, y+1]
    diagonal_lowerright = [x+1, y+1]

    if diagonal:
        adjacent_nodes = [above, below, left, right, diagonal_upperleft, diagonal_upperright, diagonal_lowerleft, diagonal_lowerright]
    else:
        adjacent_nodes = [above, below, left, right]

    legal_adjacents = [adjacent for adjacent in adjacent_nodes if 0 <= adjacent[0] < maze_length and 0 <= adjacent[1] < maze_height]

    return legal_adjacents

def return_path(current_node):
    path = []
    node_cost = 0
    current = current_node
    while current is not None:
        path.append(current.position)
        node_cost += current.f
        current = current.parent

    least_cost = {'path': path[::-1],
            'cost': node_cost}
    return least_cost 

def current_cost(current_node):
    node_cost = 0
    current = current_node
    while current is not None:
        node_cost += current.f
        current = current.parent
    return node_cost
    
def prioritise(open_list, current_node):
    list_size = len(open_list)
    if list_size == 0:
        open_list.append(current_node)
    elif current_cost(current_node) > max([current_cost(node) for node in open_list]):
        open_list.append(current_node)
    else:

        for n in range(0, list_size):
            existing_node = open_list[n]
            if current_cost(existing_node) == current_cost(current_node):
                open_list = open_list[:n + 1] + [current_node] + open_list[n + 1:]
                break
            elif current_cost(existing_node) > current_cost(current_node):
                open_list = open_list[:n] + [current_node] + open_list[n:]
                break
    
    return open_list



def astar():
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, end)

    open_list = []
    closed_list = []

    open_list.append(start_node)


    while len(open_list ) > 0 :
        current_node = open_list[0]
        open_list.pop(0)
        closed_list.append(current_node)
    
        if current_node == end_node:
            return return_path(current_node)
        else:
            next_nodes = adjacents(current_node)
            for node in next_nodes:
                new_node = Node(current_node, node)
                if len([open_node for open_node in open_list if new_node.position == open_node.position and current_cost(new_node) >= current_cost(open_node)]) > 0:
                    pass
                elif len([closed_node for closed_node in closed_list if new_node.position == closed_node.position and current_cost(new_node) >= current_cost(closed_node)]) > 0:
                    pass
                else:
                    open_list = prioritise(open_list,new_node)
                

    warn("no path found")
    return None
    
def main():
    path = astar()
    print(path)

if __name__ == '__main__':
    main()

