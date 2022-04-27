import numpy as np

def constructor(input_file):
    with open (input_file) as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]

        energy_levels = []
        positions = []

        for line in lines:
            energy = []
            for l in line:
                energy.append(int(l))

            energy_levels.append(energy)

        max_x = len(energy_levels[0])
        max_y = len(energy_levels)

        for y in range(0, max_y):
            for x in range(0, max_x):
                positions.append((x, y))


        f.close()

    energy_levels = np.array(energy_levels)

    octopus = {'energy_level': energy_levels,
                'position': positions,
                'max_x': max_x,
                'max_y': max_y
                }



    return octopus


