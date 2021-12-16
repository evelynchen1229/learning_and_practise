from construction import constructor
from collections import Counter

challenge = constructor('input.txt')

start_cave = challenge['start']

other_caves = challenge['route']
num_caves = len(other_caves)
small_cave = challenge['small_cave']

paths = []

def last_cave(path):
    caves = path.split('-')
    final_cave = caves[-1]
    return  final_cave

def first_cave(path):
    caves = path.split('-')
    beginning_cave = caves[0]
    return beginning_cave


def previous_cave(path):
    caves = path.split('-')
    previous = caves[-2]
    return previous


def connecting_caves(path,caves = other_caves):
    next_cave = []
    for cave in caves:
        
        if last_cave(path) == first_cave(cave):
            next_cave.append(cave)
    return next_cave

def small_cave_illegal_enter(path,small_caves,challenge_part):
    occurances = []
    for s_cave in small_caves:
        pattern = s_cave + '-' + s_cave
        occurance = path.count(pattern)
        occurances.append(occurance)
#    if len([o for o in occurances if o >1]) == 0:
    if max(occurances) <= 1:
        return False
    elif challenge_part == 'part2' and Counter(occurances)[2] == 1 and max(occurances) <=2:
        #len([o for o in occurances if o >1]) == 1 and max(occurances) <= 2:
        return False
    else:
        return True



def possible_routes(challenge_part,path = '', paths = [],  caves = other_caves,small_caves =small_cave ):
    associated_caves = connecting_caves(path)
    num_links = path.count('-')
    for cave in associated_caves:
        if num_links < 4:
            new_path = path + '-' + cave
            if 'end' in new_path and new_path not in paths:
                paths.append(new_path)
            else:
                paths = possible_routes(challenge_part,new_path,paths)

        elif previous_cave(path) != cave:
            if 'end' in path and path not in paths:
                paths.append(path)

            else:
                new_path = path + '-' + cave
                if small_cave_illegal_enter(new_path,small_cave,challenge_part) == True:
                    pass
                else:
                    if 'end' in new_path and new_path not in paths:
                        paths.append(new_path)
                    else:
                        if small_cave_illegal_enter(new_path,small_cave,challenge_part) == True:
                            pass
                        else:
                            paths =  possible_routes(challenge_part,new_path,paths)


    return paths

part1_total_route = 0
part1_all_paths = []

for  s in start_cave:
    s_routes = possible_routes('part1',s)
    number_routes = len(s_routes)

part1_total_route += number_routes
#part1_all_paths.append(s_routes)

print("part 1: ",part1_total_route)

part2_total_route = 0
part2_all_paths = []
for  s in start_cave:
    s_routes = possible_routes('part2',s)
    number_routes = len(s_routes)

part2_total_route += number_routes
#part2_all_paths.append(s_routes)
print("part 2: ",part2_total_route)
