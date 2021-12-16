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

    for l in route:
        if 'end' not in l:
            reverse_l = l[::-1]
            reverse_route.append(reverse_l)

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
