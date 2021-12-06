import numpy as np
from construction import construct_coordinates

# step 1: get all the coordinates for the line of vents
coordinates = construct_coordinates('input.txt')
#coordinates = construct_coordinates('test_input.txt')

'''find the size of the vent grid'''
coordinates_array = np.array(coordinates)
max_axis = coordinates_array.max()

# part 1
# focus just on the vertical or horizontal lines:
parellel_lines = []

for coordinate in coordinates:
    # coordinate structure: [x1,y1,x2,y2]
    if coordinate[0] == coordinate[2] or coordinate[1] == coordinate[-1]:
        parellel_lines.append(coordinate)

# step 2: pin on the empty vent grid
vent_grid = np.zeros((max_axis + 1,max_axis + 1))

'''mark coordinate on the vent grid'''
for coordinate in parellel_lines:
    x_1 = coordinate [0]
    y_1 = coordinate[1]
    x_2 = coordinate[2]
    y_2 = coordinate[-1]
    min_x = min(x_1,x_2)
    max_x = max(x_1,x_2)
    min_y = min(y_1,y_2)
    max_y = max(y_1,y_2)
    if x_1 == x_2:
        if max_y < max_axis:
            vent_grid[min_y:max_y + 1,x_1] += 1
        else:
            vent_grid[min_y:,x_1] += 1
    else:
        if max_x < max_axis:
            vent_grid[y_1,min_x : max_x + 1] += 1
        else:
            vent_grid[y_1,min_x : ] += 1

# step 3: find points with marked number >= 2
dangerous_area = 0
for row in vent_grid:
    for marked_number in row:
        if marked_number >= 2:
            dangerous_area += 1

print(dangerous_area)

# part 2

# focus on the diagonal lines:
diagonal_lines = []

for coordinate in coordinates:
    # coordinate structure: [x1,y1,x2,y2]
    if coordinate[0] != coordinate[2] and coordinate[1] != coordinate[-1]:
        diagonal_lines.append(coordinate)

for coordinate in diagonal_lines:
    x_1 = coordinate [0]
    y_1 = coordinate[1]
    x_2 = coordinate[2]
    y_2 = coordinate[-1]
    
    distance_x = x_1 - x_2
    distance_y = y_1 - y_2

    if x_1 > x_2:
        if y_1 > y_2:
            for (dx, dy) in zip (range(0,distance_x + 1), range(0, distance_y + 1)):
                vent_grid[ y_1 - dy,x_1 - dx] += 1
        if y_1 < y_2:
            for (dx, dy) in zip(range(0,distance_x + 1), range(0,distance_y - 1, -1)):
                vent_grid[ y_1 - dy, x_1 - dx] += 1
    if x_1 < x_2:
        if y_1 > y_2:
            for (dx, dy) in zip(range(0,distance_x - 1, -1), range(0, distance_y + 1)):
                vent_grid[y_1 - dy,x_1 - dx] += 1
        if y_1 < y_2:
            for (dx, dy) in zip(range(0,distance_x - 1, -1), range(0,distance_y - 1, -1)):
                vent_grid[y_1 - dy, x_1 - dx] += 1

dangerous_area = 0
for row in vent_grid:
    for marked_number in row:
        if marked_number >= 2:
            dangerous_area += 1

print(dangerous_area)
