def constructor(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        f.close()

    start = []
    route = []
    reverse_route = []
    small_cave = []
    for l in lines:
        if 'start' in l:
            l = l.split('-')
            position = l.index('start')
            l.pop(position)

            start.append(l[0])
        else:
            route.append(l)
    
    size_route = len(route)

    for i in range(0,size_route):
        path = route[i]
        if 'end' not in path:
            # rever the caves on a path
            # l[::-1] only works for one letter cave
            l_caves = path.split('-')
            l_caves.reverse()
            reverse_l = ('-').join(l_caves)
            reverse_route.append(reverse_l)
        else:
            end_caves = path.split('-')
            end_caves.pop(end_caves.index('end'))
            new_end_cave = end_caves[0] + '-' + 'end'
            route[i] = new_end_cave

    route = route + reverse_route

    for r in reverse_route:
        r_list = r.split('-')
        for l in r_list:
            if l.islower() and l not in small_cave:
                small_cave.append(l)

    path = {'start': start,
            'route': route,
            'small_cave':small_cave
            }

    return path


