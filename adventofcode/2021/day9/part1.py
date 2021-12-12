import numpy as np
def low_points(heightmaps):
    num_cols = len(heightmaps[0])
    num_rows = len(heightmaps)
    marked_map = np.zeros(shape=(num_rows,num_cols))

    low_points_list = []
    risk_level = []
    low_point_positions = []

    #find the lowest points in a row
    for col in range(0,num_cols):
        if col == 0:
            for row in range(0, num_rows):
                if heightmaps[row][0] < heightmaps[row][1]:
                    marked_map[row,0] += 1
        elif col == num_cols - 1:
            for row in range(0,num_rows):
                if heightmaps[row][-1] < heightmaps[row][-2]:
                    marked_map[row,-1] += 1
        else:
            for row in range(0,num_rows):
                if heightmaps[row][col] == min(heightmaps[row][col - 1 : col + 2]):
                    marked_map[row,col] += 1
        
    # find the lowest points in a column
    for row in range(0,num_rows):
        if row == 0:
            for col in range(0,num_cols):
                if heightmaps[0][col] < heightmaps[1][col]:
                    marked_map[0,col] += 1
        elif row == num_rows - 1:
            for col in range(0,num_cols):
                if heightmaps[-1][col] < heightmaps[-2][col]:
                    marked_map[-1,col] += 1
        else:
            for col in range(0,num_cols):
                if heightmaps[row][col] < heightmaps[row - 1][col] and heightmaps[row][col] < heightmaps[row + 1][col]:
                    marked_map[row,col] += 1

    # find loacations of low points
    for row in range(0,num_rows):
        mapping_list = marked_map[row]
        for col in range(0, num_cols):
            low_point_position = []
            if mapping_list[col] == 2:
                low_point = heightmaps[row][col]
                low_points_list.append(low_point)
                risk = low_point + 1
                risk_level.append(risk)
                x = col
                y = row 
                low_point_positions.append((x,y))
    part1 = {'risk':sum(risk_level),
            'low_point_positions': low_point_positions
            }            

    return part1 
