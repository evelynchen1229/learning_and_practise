def constructor(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) > 0]

        f.close()

    coordinates = []
    folding_instruction = []
    x_list = []
    y_list = []

    for l in lines:
        if 'fold' not in l:
            l_list = l.split(',')
            x = int(l_list[0])
            y = int(l_list[-1])
            coordinates.append([x,y])
            x_list.append(x)
            y_list.append(y)
        else:
            l = l.replace('fold along ','')
            fold_list = l.split('=')
            if fold_list[0] == 'y':
                y = int(fold_list[-1])
                folding_instruction.append([0,y])
            else:
                x = int(fold_list[-1])
                folding_instruction.append([x,0])
    max_x = max(x_list)
    max_y = max(y_list)

    paper = {'coordinates' : coordinates,
            'folding': folding_instruction,
            'max_x' : max_x,
            'max_y': max_y
            }

    return paper 
