from construction import constructor
#pattern_output = constructor('test_input.txt')
pattern_output = constructor('input.txt')

# part 1

unique_no_of_segments = [2,4,3,7]
unique_output = 0

for outputs in pattern_output['output']:
    for output in outputs:
        if len(output) in unique_no_of_segments:
            unique_output += 1

print(unique_output)
