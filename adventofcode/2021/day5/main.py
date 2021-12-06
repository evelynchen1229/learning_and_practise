import numpy as np
from construction import construct_coordinates

# step 1: get all the coordinates for the line of vents
coordinates = construct_coordinates('input.txt')
#coordinates = construct_coordinates('test_input.txt')

def get_coordinates(coordinates_list):
    x_1 = coordinates_list[0]
    y_1 = coordinates_list[1]
    x_2 = coordinates_list[2]
    y_2 = coordinates_list[-1]

    coordinates = {'x1': x_1,
            'y1': y_1,
            'x2': x_2,
            'y2': y_2,
            'max_x': max(x_1,x_2),
            'min_x': min(x_1,x_2),
            'max_y': max(y_1,y_2),
            'min_y': min(y_1,y_2),
            'distance_x' : x_1 - x_2,
            'distance_y' : y_1 - y_2
            }
    return coordinates

def dangerous(vent_area):
    dangerous_area = 0
    for row in vent_area:
        for marked_number in row:
            if marked_number >= 2:
                dangerous_area += 1

    return dangerous_area

'''find the size of the vent grid'''
coordinates_array = np.array(coordinates)
max_axis = coordinates_array.max()

# part 1
# focus just on the vertical or horizontal lines:
straight_lines = []

for coordinate in coordinates:
    line = get_coordinates(coordinate)
    if line['x1'] == line['x2'] or line['y1'] == line['y2']:
        straight_lines.append(coordinate)

# step 2: pin on the empty vent grid
vent_grid = np.zeros((max_axis + 1,max_axis + 1))

'''mark coordinate on the vent grid'''
for coordinate in straight_lines:
    line = get_coordinates(coordinate)
    if line['x1'] == line['x2']:
        if line['max_y'] < max_axis:
            vent_grid[line['min_y'] : line['max_y'] + 1, line['x1']] += 1
        else:
            vent_grid[line['min_y'] : , line['x1']] += 1
    else:
        if line['max_x'] < max_axis:
            vent_grid[line['y1'], line['min_x'] : line['max_x'] + 1] += 1
        else:
            vent_grid[line['y1'], line['min_x' : ]] += 1

# step 3: find points with marked number >= 2
dangerous_area = dangerous(vent_grid) 
print(dangerous_area)

# part 2

# focus on the diagonal lines:
diagonal_lines = []

for coordinate in coordinates:
    line = get_coordinates(coordinate)
    if line['x1'] != line['x2'] and line['y1'] != line['y2']:
        diagonal_lines.append(coordinate)

for coordinate in diagonal_lines:
    line = get_coordinates(coordinate)
    if line['x1'] > line['x2']:
        if line['y1'] > line['y2']:
            for (dx, dy) in zip (range(0, line['distance_x'] + 1), range(0, line['distance_y'] + 1)):
                vent_grid[line['y1'] - dy, line['x1'] - dx] += 1
        else:
            for (dx , dy) in zip(range(0, line['distance_x'] + 1), range(0, line['distance_y'] -1, -1)):
                vent_grid[line['y1'] - dy, line['x1'] - dx] += 1
    else:
        if line['y1'] > line['y2']:
            for (dx,dy) in zip(range(0, line['distance_x'] -1, -1), range(0, line['distance_y'] + 1)):
                vent_grid[line['y1'] - dy, line['x1'] - dx] += 1
        else:
            for (dx, dy) in zip(range(0, line['distance_x'] -1, -1), range(0, line['distance_y'] -1, -1)):
                vent_grid[line['y1'] - dy, line['x1'] - dx] += 1


dangerous_area = dangerous(vent_grid) 
print(dangerous_area)
