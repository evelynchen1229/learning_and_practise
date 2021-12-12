from construction import constructor
import numpy as np

#heightmaps = constructor('test_input.txt')
heightmaps = constructor('input.txt')
#print(heightmaps)

low_points = []
risk_level = []

num_cols = len(heightmaps[0])
num_rows = len(heightmaps)

# part 1
# lowest points have both row and column value 1, i.e. index value equals 2 then it's the lowest point
marked_map = np.zeros(shape=(num_rows,num_cols))
#print(marked_map)

# find the lowest points in a row
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

#print(marked_map)

#print(marked_map[0])
low_point_positions = []
for row in range(0,num_rows):
    low_point_position = []
    mapping_list = marked_map[row]
    for col in range(0, num_cols):
        low_point_position = []
        if mapping_list[col] == 2:
            low_point = heightmaps[row][col]
            risk = low_point + 1
            low_points.append(low_point)
            risk_level.append(risk)
            low_point_position.append(row)
            low_point_position.append(col)
            low_point_positions.append(low_point_position)
            
#print(lowest_points)
print(sum(risk_level))
#print(low_point_positions)

# part 2
#for row in range(0, num_rows):
#    for col in range(0, num_cols):
#        if heightmaps[row][col] == 9:
#            marked_map[row,col] = -1
#print(marked_map)

basins = []
basin_points = []


for low_point_position in low_point_positions:
    print(low_point_position)
    basin_size = 0
    col = low_point_position[1]
    row = low_point_position[0]
    low_point = heightmaps[row][col]
    print(low_point)
    # for each low point, find the lower and upper column of the basin
    # probelm: lower and upper columns is not based on the lower point row
    for i in range(col,-1,-1):
        if heightmaps[row][i] != 9 and heightmaps[row][i] >= low_point and [row,i] not in basin_points:
            print(heightmaps[row][i])
            basin_size += 1
            basin_points.append([row,i])
            if i == 0:
                start_column = 0
        else:
            start_column = i + 1
            break

    for i in range(col, num_cols):
        if heightmaps[row][i] != 9 and heightmaps[row][i] >= low_point:
            print(heightmaps[row][i])
            if [row,i] not in basin_points:
                basin_size += 1
                basin_points.append([row,i])
            else:
                pass
            if i == num_cols - 1:
                end_column = i

        else:
            end_column = i - 1
            break

    for column in range(start_column, end_column + 1):
        if column == start_column:
            if row == 0:
                for r in range(1, num_rows):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        basin_size += 1
                        basin_points.append([r,column])
                        for c in range(0,start_column):
                            if start_column == 0:
                                pass
                            else:
                                if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points:
                                    print(heightmaps[r][c])
                                    basin_size += 1
                                    basin_points.append([r,c])
                                else:
                                    break
                    else:
                        break
            elif row == num_rows - 1:
                for r in range(row - 1, -1, -1):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        basin_size += 1
                        print(heightmaps[r][column])
                        basin_points.append([r,column])

                        for c in range(0,start_column):
                            if start_column == 0:
                                pass
                            else:
                                if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points :
                                    print(heightmaps[r][c])
                                    basin_size += 1
                                    basin_points.append([r,c])
                                else:
                                    break
                    else:
                        break
            else:
                for r in range(row + 1, num_rows):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        basin_size += 1
                        basin_points.append([r,column])
                        for c in range(0,start_column):
                            if start_column == 0:
                                pass
                            else:
                                if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points :
                                    basin_size += 1
                                    print(heightmaps[r][c])
                                    basin_points.append([r,c])
                                else:
                                    break
                    else:
                        break
    
                for r in range(row - 1, -1, -1):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        basin_size += 1
                        print(heightmaps[r][column])
                        basin_points.append([r,column])
                        for c in range(0,start_column):
                            if start_column == 0:
                                pass
                            else:
                                if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points: 
                                    basin_size += 1
                                    print(heightmaps[r][c])
                                    basin_points.append([r,c])
                                else:
                                    break
                    else:
                        break

    
        elif column == end_column and column != num_cols - 1:
            if row == 0:
                for r in range(1, num_rows):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        for c in range(end_column ,num_cols):
                            if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points:
                                print(heightmaps[r][c])
                                basin_size += 1
                                basin_points.append([r,c])
                            else:
                                break
                    else:
                        break
            elif row == num_rows - 1:
                for r in range(row - 1, -1, -1):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        for c in range(end_column ,num_cols):
                            if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points:
                                print(heightmaps[r][c])
                                basin_size += 1
                                basin_points.append([r,c])
                            else:
                                break
                    else:
                        break
            else:
                for r in range(row + 1, num_rows):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points:
                        print(heightmaps[r][column])
                        for c in range(end_column ,num_cols):
                            if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points:
                                print(heightmaps[r][c])
                                basin_size += 1
                                basin_points.append([r,c])
                            else:
                                break
                    else:
                        break
    
                for r in range(row - 1, -1, -1):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        for c in range(end_column ,num_cols):
                            if heightmaps[r][c] != 9 and heightmaps[r][c] >= low_point and [r,c] not in basin_points:
                                print(heightmaps[r][c])
                                basin_size += 1
                                basin_points.append([r,c])
                            else:
                                break
                    else:
                        break
        else:

            if row == 0:
                for r in range(1, num_rows):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        basin_size += 1
                        basin_points.append([r,column])
                    else:
                        break
            elif row == num_rows - 1:
                for r in range(row - 1, -1, -1):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points:
                        print(heightmaps[r][column])
                        basin_size += 1
                        basin_points.append([r,column])
                    else:
                        break
            else:
                for r in range(row + 1, num_rows):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points :
                        print(heightmaps[r][column])
                        basin_size += 1
                        basin_points.append([r,column])
                    else:
                        break
    
                for r in range(row - 1, -1, -1):
                    if heightmaps[r][column] != 9 and heightmaps[r][column] >= low_point and [r,column] not in basin_points:
                        print(heightmaps[r][column])
                        basin_size += 1
                        basin_points.append([r,column])
                    else:
                        break
    
    basins.append(basin_size)

print(basin_points)
print(basins)
basins.sort(reverse=True)
print(basins)
largest_basins = basins[0] * basins[1] * basins[2]
print(largest_basins)
