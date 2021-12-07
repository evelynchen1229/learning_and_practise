def constructor(position_file):
    position = []
    with open(position_file) as f:
        lines = f.readlines()
        position_line = lines[0].strip().split(',')
        for p in position_line:
            position.append(int(p))
    return position
    
