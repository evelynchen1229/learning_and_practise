def constructor(file_name):
    entry_output = []

    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            patterns = []
            outputs = []
            pattern_output = {}
            line = line.strip()
            line = line.split('|')
            pattern_line = line[0].split(' ')[0:-1]
            output_line = line[-1].split(' ')[1:]
            for pattern in pattern_line:
                patterns.append(pattern)
            for output in output_line:
                outputs.append(output)
            
            pattern_output = {'pattern':patterns,
                    'output': outputs}
            entry_output.append(pattern_output)

        f.close()

    return entry_output

            
            

            


