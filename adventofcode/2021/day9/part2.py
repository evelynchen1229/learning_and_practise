from construction import constructor
from part1 import low_points
import numpy as np

test_heightmaps = constructor('test_input.txt')
challenge_heightmaps = constructor('input.txt')

test_low_points = low_points(test_heightmaps)['low_point_positions']
challenge_low_points = low_points(challenge_heightmaps)['low_point_positions']

#print(test_low_points)

maxium_x = len(challenge_heightmaps[0])
maxium_y = len(challenge_heightmaps)


def adjacent_points(point_position, max_x = maxium_x - 1, max_y = maxium_y - 1):
    x = point_position[0]
    y = point_position[1]
    left =  (x - 1, y) 
    right = (x + 1, y)
    above = (x, y - 1)
    below = (x, y + 1)
    four_points = [left, right, above, below]
    legal_four_points = [point for point in four_points if 0 <= point[0] <= max_x and 0 <= point[1] <= max_y]
    
    return legal_four_points 

def flatten(array):
    result = []
    for i in range(len(array)):
        result += array[i]
    return result

def dedup(result):
    dedupped_list = []
    for a in result:
        if a not in dedupped_list:
            dedupped_list.append(a)

    return dedupped_list

def basin(center_point, heightmap, basin_list = [], depth = 0):
    center_point_row = center_point[1]
    center_point_col = center_point[0]
    center_point_height = heightmap[center_point_row][center_point_col]

    points_around_point = adjacent_points(center_point)
    additional_points = [point for point in points_around_point if heightmap[point[1]][point[0]] < 9 and heightmap[point[1]][point[0]] >= center_point_height and point not in basin_list]

    #additional_points = filter points_around_point: height < 9 and height >= low_point_height and height not in basin_list

#    print("depth=", depth)
#    print("basin list: ", basin_list)
#    print("additional points", additional_points)
    points_with_additional = basin_list + additional_points
#    print("points with additional: ", points_with_additional)

    return dedup([center_point] + flatten([basin(point, heightmap, points_with_additional, depth + 1) for point in additional_points]))
    #return points_with_additional + (map additional_points basin(point, heightmap, points_with_additional))
    
#test = basin((9,0),test_heightmaps)
#print(test)
basins_size = []
#print(len(challenge_low_points))
for low_point in challenge_low_points:
    basin_result = basin(low_point,challenge_heightmaps)
    basins_size.append(len(basin_result))
#print(basins_size)
basins_size.sort(reverse=True)
part2 = basins_size[0] * basins_size[1] * basins_size[2]
print(part2)
