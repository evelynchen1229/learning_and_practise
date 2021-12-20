def constructor(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        f.close()

    graph = []

    for line in lines:
        vertex = []
        for l in line:
            vertex.append(int(l))

        graph.append(vertex)

    return graph
