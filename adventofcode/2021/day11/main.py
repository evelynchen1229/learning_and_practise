from construction import constructor
import numpy as np

test_lines = constructor('test_input.txt')
sample_lines = constructor('sample.txt')

cols = test_lines['max_x']
rows = test_lines['max_y']

def adjacent(position):
    print(position)
    #print(position)
    x = position[0]
    y = position[1]

    left = (x-1, y)
    right = (x+1, y)
    above = (x, y-1)
    below = (x, y+1)
    upper_left = (x-1, y+1)
    upper_right = (x+1, y+1)
    down_left = (x-1, y-1)
    down_right = (x+1, y-1)

    adjacent_positions = [left, right, above, below, upper_left, upper_right, down_left, down_right]

    legal_adjacents = [p for p in adjacent_positions if 0 <= p[0] < cols and 0 <= p[1] < rows]

    return legal_adjacents

def energy_number(position,level_map):
    row = position[1]
    col = position[0]
    return level_map[row][col]

def flash_level_list( energy_level_map):
    flashy = []
    for row in range(0, rows):
        for col in range(0, cols):
            if energy_level_map[row][col] == 10:
                #print((col,row))
                flashy.append((col, row))
    print("flasy:",flashy)
    return flashy


def adjacent_level_increase(flash_position, energy_level_map):
    for flash_point in flash_position:
        print(flash_point)
        adjacent_positions = adjacent(flash_point)

        new_flash = []
   #       print("adjacents:",adjacent_positions)
        for adjacent_position in adjacent_positions:
            adjacent_row = adjacent_position[1]
            adjacent_col = adjacent_position[0]
   #         print("adjacents point:", adjacent_position)
   #         print("adjacent energy:", energy_number(adjacent_position, energy_level_map))

            if  energy_number(adjacent_position, energy_level_map) < 10:
                energy_level_map[adjacent_row][adjacent_col] += 1
                adjacent_energy = energy_level_map[adjacent_row][adjacent_col]#energy_number(adjacent_position, energy_level_map)
                if adjacent_energy == 10:
                    print(adjacent_position)
                    new_flash.append(adjacent_position)
                    print(new_flash)
                else:
                    pass
            else:
                pass
        print(new_flash)
        if len(new_flash) == 0:
            print("yes")
            return energy_level_map
        else:
            return adjacent_level_increase(new_flash, energy_level_map)
   # return energy_level_map


def flash( energy_level_map , position ):
    'level increase by 1 in the beginning of the step'
    energy_level_map += 1
    print("energy map",energy_level_map)

    'find all the original flash level'
    flash_points = flash_level_list(energy_level_map)
    print("flash points",flash_points)
    #print(flash_points)
    '''find all the adjacent points for the flash points
    adjacent level increase by 1
    if any adjacent level reach flash points - repeat process until no adjacent level is flashy
    '''
    for p in flash_points:
#        print(p)
        energy_level_map = adjacent_level_increase([p],energy_level_map)

    energy_level_map = np.where(energy_level_map == 10, 0, energy_level_map)

#    after_n_steps = {'new_energy': energy_level_map,
#            'num_of_flashes': flashes
 #           }

    return energy_level_map

def num_flash(step, energy_level_map = sample_lines['energy_level'],  position = sample_lines['position']):
    flashes = 0
    for s in range(0, step):
        energy_level_map = flash(energy_level_map, position)
        print(energy_level_map)
        flashes += np.count_nonzero(energy_level_map == 0)

    return flashes

#test = flash()#, test_lines, test_lines['energy_level'], test_lines['position'])
test_flashes = num_flash(2, test_lines['energy_level'],test_lines['position'])
print(test_flashes)
#print(test)







