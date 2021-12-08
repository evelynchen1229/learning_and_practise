def constructor(file_name):
    pattern_sets = []
    output_sets = []

    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            patterns = []
            outputs = []
            line = line.strip()
            line = line.split('|')
            pattern_line = line[0].split(' ')[0:-1]
            output_line = line[-1].split(' ')[1:]
            for (pattern, output) in zip(pattern_line, output_line):
                patterns.append(pattern)
                outputs.append(output)
        
            pattern_sets.append(patterns)
            output_sets.append(outputs)

        f.close()
    entry_output = {'pattern' : pattern_sets,
            'output' : output_sets
            }
    return entry_output

            
            

            


