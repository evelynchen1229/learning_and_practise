from construction import constructor

test = constructor('small_sample.txt')

print(test)

start_cave = test['start']

other_caves = test['route']
num_caves = len(other_caves)
small_cave = test['small_cave']
print(small_cave)

paths = []

def connecting_caves(path,caves = other_caves):
    next_cave = []
    for cave in caves:
        if path[-1] == cave[0]:
            next_cave.append(cave)
    return next_cave


def possible_routes(path = '', paths = [],  caves = other_caves):
    print(path)
    associated_caves = connecting_caves(path)
    num_links = path.count('-')
    print("associated_caves",associated_caves)
    for cave in associated_caves:
        print(cave)
        if num_links < 4:
            print("link less than 4")
            new_path = path + '-' + cave
            print(new_path)
            if 'end' in new_path and new_path not in paths:
                paths.append(new_path)
                print("initial path",paths)
            else:
                paths = possible_routes(new_path,paths)
        elif path[-7:-4] != cave:
            print("path for link more than 4",path)
            print(cave)
            if 'end' in path and path not in paths:
                paths.append(path)

            else:
                print("path",path)
                new_path = path + '-' + cave
                if 'end' in new_path and new_path not in paths:
                    paths.append(new_path)
                else:
                    if (cave.islower() == True or (cave.islower() == False and cave.isupper() == False) ) and cave in path:
                        print("repeated",cave,new_path)
                        pass
                    else:
                        paths =  possible_routes(new_path,paths)
 #       print("after loop",path)

    #else:
     #   print("path loop",path)
     #   paths = possible_routes(path)
    print("final paths",paths)


    return paths
#    for n in range(starting_point,num_caves):
#        print(caves[n])
#        if path[-1] == caves[n][0] and caves[n] != path[-7:-4]:
#            print("caves associated",caves[n])
#            path = path + '-' + caves[n]
#            print(path)
#            if 'end' in caves[n] and path not in paths:
#                paths.append(path)
#            else:
#               return possible_routes(path,caves)
#
#
#    print(paths)
#
#
#    return paths
#
test_route = possible_routes('b')
#print(test_route)
num_routes = 0
legal_routes_b = []
for  r in test_route:

    occurances = []
    for s_cave in small_cave:
        pattern = s_cave + '-' + s_cave
        occurance = r.count(pattern)
        occurances.append(occurance)
    if len([o for o in occurances if o >1]) == 0:
        num_routes += 1
        legal_routes_b.append(r)
    else:
        print (r)
print(num_routes)
print(legal_routes_b)


test_route = possible_routes('A')
#print(test_route)
num_routes = 0
legal_routes_a = []
for  r in test_route:

    occurances = []
    for s_cave in small_cave:
        pattern = s_cave + '-' + s_cave
        occurance = r.count(pattern)
        occurances.append(occurance)
    if len([o for o in occurances if o >1]) == 0:
        num_routes += 1
        legal_routes_a.append(r)
    else:
        print (r)
print(num_routes)
print(legal_routes_a)
