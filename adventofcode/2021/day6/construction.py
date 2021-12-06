def constructor(file_name):
    initial_state = []
    with open(file_name) as f:
        line = f.readlines()[0].strip().split(',')
        for l in line:
            initial_state.append(int(l))

    return initial_state


