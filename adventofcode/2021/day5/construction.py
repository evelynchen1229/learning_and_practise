# for each number set, put four numbers in a list
def get_coordinates (point_on_line):
    coordinates = point_on_line.split(',')
    x_coordinate = int(coordinates[0])
    y_coordinate = int(coordinates[-1])
    coordinates = {'x': x_coordinate,
            'y': y_coordinate
            }
    return coordinates

def construct_coordinates(file_for_lines_of_vents):
    coordinates = []
    with open(file_for_lines_of_vents) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(' ')
            line.pop(1)
            # put coordinate of one line into a list
            start_point = line[0]
            end_point = line[-1]

            x_1 = get_coordinates(start_point)['x']
            y_1 = get_coordinates(start_point)['y']
            x_2 = get_coordinates(end_point)['x']
            y_2 = get_coordinates(end_point)['y']

            coordinate = [x_1,y_1,x_2,y_2]
            
            coordinates.append(coordinate)

    return coordinates 
