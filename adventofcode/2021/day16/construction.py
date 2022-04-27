def constructor(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        f.close()

    transmission = []
    for line in lines:
        for l in line:
            if type(l) == int:
                transmission.append(int(l))
            else:
                transmission.append(l)

    return transmission
