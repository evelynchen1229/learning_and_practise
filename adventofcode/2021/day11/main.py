from construction import constructor
import numpy as np

test_lines = constructor('test_input.txt')
sample_lines = constructor('sample.txt')
challenge_lines = constructor('input.txt')

cols = challenge_lines['max_x']
rows = challenge_lines['max_y']

def adjacent(position):
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
                flashy.append((col, row))
    return flashy

def adjacent_level_increase(flash_position, energy_level_map):
    adjacent_positions = adjacent(flash_position)

    new_flashes = []
    for adjacent_position in adjacent_positions:
        adjacent_row = adjacent_position[1]
        adjacent_col = adjacent_position[0]

        if  energy_number(adjacent_position, energy_level_map) < 10:
            energy_level_map[adjacent_row][adjacent_col] += 1
            adjacent_energy = energy_number(adjacent_position, energy_level_map)

            if adjacent_energy == 10:
                new_flashes.append(adjacent_position)

    if len(new_flashes) == 0:
        return energy_level_map
    elif len(new_flashes) == 1:
        return adjacent_level_increase(new_flashes[0], energy_level_map)
    else:
        for new_flash in new_flashes:
            enery_level_map = adjacent_level_increase(new_flash, energy_level_map)

    return energy_level_map

def flash( energy_level_map , position ):
    'level increase by 1 in the beginning of the step'
    energy_level_map += 1

    'find all the original flash level'
    flash_points = flash_level_list(energy_level_map)

    '''find all the adjacent points for the flash points
    adjacent level increase by 1
    if any adjacent level reach flash points - repeat process until no adjacent level is flashy
    '''
    for p in flash_points:
        energy_level_map = adjacent_level_increase(p,energy_level_map)

    energy_level_map = np.where(energy_level_map == 10, 0, energy_level_map)

    return energy_level_map

def num_flash(step, energy_level_map = sample_lines['energy_level'],  position = sample_lines['position']):
    flashes = 0
    for s in range(0, step):
        energy_level_map = flash(energy_level_map, position)
        flashes += np.count_nonzero(energy_level_map == 0)

    return flashes

def syncronise(step = 0,energy_level_map = test_lines['energy_level'],position = test_lines['position']):
    num_flashes = 0
    while num_flashes < 100:
         energy_level_map = flash(energy_level_map,position)
         num_flashes = np.count_nonzero(energy_level_map == 0)
         step += 1
    return step

'''part 1'''
challange_flashes = num_flash(100, challenge_lines['energy_level'],challenge_lines['position'])
print("part 1:",challange_flashes)

'''part 2'''
challenge_all_flash = syncronise(energy_level_map = challenge_lines['energy_level'],position=challenge_lines['position'])
print("part2:", challenge_all_flash)







