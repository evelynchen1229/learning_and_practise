def constructor(input_file):
    with open(input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        f.close()

    graph_value = []

    for line in lines:
        vertex = []
        for l in line:
            vertex.append(int(l))

        graph_value.append(vertex)

    num_rows = len(graph_value)
    num_cols = len(graph_value[0])

    graph_position = []
    for col in range(0, num_cols):
        for row in range(0, num_rows):
            graph_position.append([col, row])

    graph = {'values' : graph_value,
            'position': graph_position
            }





    return graph
