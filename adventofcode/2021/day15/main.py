'''
A-star algorithm
F = G + H

F is the total cost of the node.
G is the distance between the current node and the start node.
H is the heuristic — estimated distance from the current node to the end node.

1. Add the starting square (or node) to the open list.
2. Repeat the following:
A) Look for the lowest F cost square on the open list. We refer to this as the current square.
B). Switch it to the closed list.
C) For each of the 8 squares adjacent to this current square …
If it is not walkable or if it is on the closed list, ignore it. Otherwise do the following.
If it isn’t on the open list, add it to the open list. Make the current square the parent of this square. Record the F, G, and H costs of the square.
If it is on the open list already, check to see if this path to that square is better, using G cost as the measure. A lower G cost means that this is a better path. If so, change the parent of the square to the current square, and recalculate the G and F scores of the square. If you are keeping your open list sorted by F score, you may need to resort the list to account for the change.
D) Stop when you:
Add the target square to the closed list, in which case the path has been found, or
Fail to find the target square, and the open list is empty. In this case, there is no path.
3. Save the path. Working backwards from the target square, go from each square to its parent square until you reach the starting square. That is your path.
'''

# import heap queue for priority queue
import heapq
from warnings import warn

class Node():
    '''A Node class for A* pathfinding'''

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

     def __eq__(self, other):
         return self.position == other.position

     def __repr(self):
         return f"{self.position} - g : {self.g} h: : {self.h} f: {self.f}"

     # define less than
     def __lt__(self, other):
         return self.f < other.f

     # define greater than
     def __gt__(slef,other):
         return self.f > other.f

def return_path(current_code):
    path = []
    current = current_code
    while current is not None:
        path.append(current.position)

    return path[::-1]

def astar(maze, start, end):
    ''' returns a list of tuples as path'''

    '''
    // initialise both open and closed lists
    let open list an empty list of nodes
    let closed list an empty list of nodes

    // Add start node into open list, leave f to 0
    '''
        # create a start, end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0

    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0


    # create empty open closed lists
    open_list = []
    closed_list = []

    # add start node
    heapq.heapify(open_list)
    heapq.heappush(open_list, start_node)

    # adding a stop condition
    outer_iteration = 0
    max_iteration = (len(maze[0]) * len(maze)) // 2

    # adjacent nodes for whether diagnoal nodes allowable 
    adjacent_nodes = ((0,-1), (0,1), (1,0), (-1,0))
    
    if diagnoal_allowed:
        adjacent_nodes = ((0,-1), (0,1), (1,0), (-1,0), (-1,-1), (-1,1), (1, -1), (1,1),)

    '''
    // Loop until find the end
    whie open_list is not empty
        // get current node
        // find end node
        // if next node isn't end node, get all possible next steps - generate children
        // add current node as parent, within children, calculate cost (f, g, h) for all the next steps and add to the heap queue
            child.g = cost from start to child node,
            child.h = cost from child node to end
            child.f = child.g + child.f

        // check whether child is alredy in open list (find cheaper way to go to the same child node)
            if child already in open list:
                if child.f > existing.f: 
                    then pass
                else:
                    add child to the open_list
    '''

    while len(open_list) > 0:
        outer_iteration += 1
        
        if outer_iteration > max_iteration:
            warn("too many iterations")
            return current_node

        # get the current node
        current_node = heapq.heappop(open_list)
        closed_list.append(current_node)

        # find the goal
        if current_node == end_node:
            return return_path(current_code)

        # generate children
        children = []
        for new_position in adjacent_position:
            # get only legal adjacents
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            if node_position[0] < 0 or node_position[0] >= len(maze[0]) or node_position[1] < 0 or node_position[1] >= len(maze):
                pass

            new_node = Node(current_node, node_position)
            children.append(new_node)

        # loop through children
        for child in children:
            # whether child in closed list
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                pass

            child.g = current_node.g + 1
            child.h = (child.position[0] - end_node.position[0]) ** 2 + (child.position[1] - end_node.position[1]) ** 2
            child.f = child.g + child.h

            # whether child in open list
            if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                pass

            heapq.heappush(open_list, child)
    warn ("couldn't get a path")
    return None


