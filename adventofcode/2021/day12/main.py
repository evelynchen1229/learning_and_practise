from construction import constructor

test = constructor('input.txt')

#print(test)

start_cave = test['start']

other_caves = test['route']
print(other_caves)
num_caves = len(other_caves)
small_cave = test['small_cave']
#print(small_cave)

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
        # to find the connecting point, so the end cave of current path is the same as the begining cave of the next path
        # path[-1] only works for one letter cave
        
        if last_cave(path) == first_cave(cave):
            next_cave.append(cave)
    return next_cave


def possible_routes(path = '', paths = [],  caves = other_caves):
    #print(path)
    associated_caves = connecting_caves(path)
    num_links = path.count('-')
   # print("associated_caves",associated_caves)
    for cave in associated_caves:
        #print(cave)
        if num_links < 4:
          #  print("link less than 4")
            new_path = path + '-' + cave
         #   print(new_path)
            if 'end' in new_path and new_path not in paths:
                paths.append(new_path)
        #        print("initial path",paths)
            else:
                paths = possible_routes(new_path,paths)

        # make sure cave the previous cave isn't the same 
        # pth[-7:-4] only works with one letter cave
        elif previous_cave(path) != cave:
      #      print("path for link more than 4",path)
       #     print(cave)
            if 'end' in path and path not in paths:
                paths.append(path)

            else:
     #           print("path",path)
                new_path = path + '-' + cave
                if 'end' in new_path and new_path not in paths:
                    paths.append(new_path)
                else:
                    if (cave.islower() == True or (cave.islower() == False and cave.isupper() == False) ) and cave in path:
    #                    print("repeated",cave,new_path)
                        pass
                    else:
                        paths =  possible_routes(new_path,paths)
    #print("final paths",paths)


    return paths

def legal_routes(start_cave,path = '', paths = [],caves = other_caves):
    all_routes = possible_routes(start_cave)
    num_routes = 0
    legal_routes_list = []
    for  r in all_routes:
        occurances = []
        for s_cave in small_cave:
            pattern = s_cave + '-' + s_cave
            occurance = r.count(pattern)
            occurances.append(occurance)
        if len([o for o in occurances if o >1]) == 0:
            num_routes += 1
            legal_routes_list.append(r)
    
    legal_route = {'number of legal routes':num_routes,
            'legal routes':legal_routes_list
            }
    
    return legal_route

s = legal_routes('DX')
print(s)

total_route = 0
all_paths = []

#for  s in start_cave:
#    print(s)
#    s_routes = legal_routes(s)
#    number_routes = s_routes['number of legal routes']
#    #print(number_routes)
#    legal_paths = s_routes['legal routes']
#   # print(legal_paths)
#
#total_route += number_routes
#all_paths.append(legal_paths)
#
#print(total_route,all_paths)
#
##    for n in range(starting_point,num_caves):

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
#test_route = possible_routes('b')
##print(test_route)
#num_routes = 0
#legal_routes_b = []
#for  r in test_route:
#
#    occurances = []
#    for s_cave in small_cave:
#        pattern = s_cave + '-' + s_cave
#        occurance = r.count(pattern)
#        occurances.append(occurance)
#    if len([o for o in occurances if o >1]) == 0:
#        num_routes += 1
#        legal_routes_b.append(r)
#    else:
#        print (r)
#print(num_routes)
#print(legal_routes_b)
#
#
#test_route = possible_routes('A')
##print(test_route)
#num_routes = 0
#legal_routes_a = []
#for  r in test_route:
#
#    occurances = []
#    for s_cave in small_cave:
#        pattern = s_cave + '-' + s_cave
#        occurance = r.count(pattern)
#        occurances.append(occurance)
#    if len([o for o in occurances if o >1]) == 0:
#        num_routes += 1
#        legal_routes_a.append(r)
#    else:
#        print (r)
#print(num_routes)
#print(legal_routes_a)
