import numpy as np
def fullmaze(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        f.close()

    graph_value = []

    for line in lines:
        vertex = []
        for l in line:
            vertex.append(int(l))

        graph_value.append(vertex)

    num_rows = len(graph_value)
    num_cols = len(graph_value[0])


    maze = np.array(graph_value)
    maze.shape = (num_rows,num_cols)
    new_maze = maze

    for n in range(1,5):
        add_maze = maze + n
        
        new_maze = np.concatenate((new_maze,add_maze),axis = 0)

    full_maze = new_maze

    for n in range(1,5):
        add_maze = new_maze + n
        
        full_maze = np.concatenate((full_maze,add_maze),axis = 1)

    full_maze = np.where(full_maze > 9, full_maze - 9, full_maze)
    
    num_full_rows = len(full_maze)
    num_full_cols = len(full_maze[0])
    maze_position = []
    for col in range(0, num_full_cols):
        for row in range(0, num_full_rows):
            maze_position.append([col, row])

    complete_maze = {'values':full_maze,
            'position': maze_position
            }
        
    return complete_maze 



