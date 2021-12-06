coordinates = [
        [1,1,1,3],
        [9,7,7,7],
        [1,1,3,3],
        [9,7,7,9],
        [6,4,2,0]

        ]

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
                print([x_1 - dx, y_1 - dy])
        if y_1 < y_2:
            for (dx, dy) in zip(range(0,distance_x + 1), range(0,distance_y - 1, -1)):
                print([x_1 - dx, y_1 - dy])
    if x_1 < x_2:
        if y_1 > y_2:
            for (dx, dy) in zip(range(0,distance_x - 1, -1), range(0, distance_y + 1)):
                print([x_1 - dx, y_1 - dy])
        if y_1 < y_2:
            for (dx, dy) in zip(range(0,distance_x - 1, -1), range(0,distance_y - 1, -1)):
                print([x_1 - dx, y_1 - dy])

