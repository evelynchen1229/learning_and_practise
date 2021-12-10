def constructor(location_file):
    locations = []
    with open(location_file) as f:
        lines = f.readlines()
        for line in lines:
            location = []
            line = line.strip()
            for l in line:
                location.append(int(l))
            locations.append(location)
    f.close()

    return locations
