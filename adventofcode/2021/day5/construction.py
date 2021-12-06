# for each number set, put four numbers in a list
def construct_coordinates(file_for_lines_of_vents):
    coordinates = []
    with open(file_for_lines_of_vents) as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip().split(' ')
            line.pop(1)
            # put coordinate of one line into a list
            start_point = line[0].split(',')
            x_1 = int(start_point[0])
            y_1 = int(start_point[-1])
    
            end_point = line[-1].split(',')
            x_2 = int(end_point[0])
            y_2 = int(end_point[-1])
    
            coordinate = [x_1,y_1,x_2,y_2]
            
            coordinates.append(coordinate)

    return coordinates 
