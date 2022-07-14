def constructor(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = [line for line in lines if len(line) >0]

        f.close
    polymer = lines[0]
    pair = []
    for line in lines[1:]:
        line_list = line.split(' -> ')
        pair.append(line_list)
    insertion = {'polymer':polymer,
            'pair_rule' : pair
            }

    return insertion
