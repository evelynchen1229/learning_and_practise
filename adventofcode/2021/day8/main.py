from construction import constructor
#entries = constructor('test_input.txt')
entries = constructor('input.txt')
#entries = constructor('sample.txt')

# part 1

unique_no_of_segments = [2,4,3,7]
unique_output = 0
size = len(entries)

for num in range(0, size):
    entry = entries[num]
    for output in entry['output']:
        if len(output) in unique_no_of_segments:
            unique_output += 1
    
print(unique_output)

# part 2
def find_digits(pattern_output):
    signal_patterns = [
            [1,1,1,0,1,1,1],
            [0,0,1,0,0,1,0],
            [1,0,1,1,1,0,1],
            [1,0,1,1,0,1,1],
            [0,1,1,1,0,1,0],
            [1,1,0,1,0,1,1],
            [1,1,0,1,1,1,1],
            [1,0,1,0,0,1,0],
            [1,1,1,1,1,1,1],
            [1,1,1,1,0,1,1]
            ]
    position = [1,2,3,4,5,6,7]
    
    seven = ''
    one = ''
    four = ''
    six = ''
    eight = ''
    nine = ''
    zero=''
    six_nine_zero = []
    two_three_five = []

    for pattern in pattern_output['pattern']:
        if len(pattern) == 3:
            seven = pattern
        elif len(pattern) == 2:
            one = pattern
        elif len(pattern) == 4:
            four = pattern
        elif len(pattern) == 7:
            eight = pattern
        elif len(pattern) == 6:
            six_nine_zero.append(pattern)
    
    # find pattern for a
    seven_four = seven + four
    for letter in seven:
        if letter not in one:
            position[0] = letter
    
    #find nine
    #find pattern for g
    for pattern in six_nine_zero:
        missing_segment  = []
        for letter in pattern:
            if letter not in seven_four:
                missing_segment.append(letter)
        if len(missing_segment) == 1:
            nine = pattern
            position[-1] = missing_segment[0]
    
    #find pattern for e
    for letter in eight:
        if letter not in nine:
            position[-3] = letter
    
    # find zero
    # find pattern for d
    for pattern in six_nine_zero:
        if pattern != nine and pattern.count(one[0]) > 0 and pattern.count(one[-1]) > 0:
            zero = pattern
            for letter in four:
                if letter not in zero:
                    position[3] = letter
    
    # find six
    # find pattern for b
    for pattern in six_nine_zero:
        if pattern != nine and (pattern.count(one[0]) == 0 or pattern.count(one[-1]) == 0) :
            six = pattern
            for letter in six:
                if letter not in [position[-3], position[3],position[-1]] and letter not in seven:
                    position[1] = letter
    
    # find pattern for c
    for letter in four:
        if letter not in six:

            position[2] = letter
    
    #find pattern for f
    for letter in one:
        if letter != position[2]:
            position[-2] = letter


    digits = ''
    for output in pattern_output['output']:
        signal_pattern = [0] * 7
        for letter in output:
            location = position.index(letter)
            signal_pattern[location] = 1
        digit = str(signal_patterns.index(signal_pattern))
        digits += digit
    total = int(digits)

    return total

output_digits = []
size = len(entries)

for num in range(0, size):
    entry = entries[num]
    output_digit = find_digits(entry)
    output_digits.append(output_digit)

print(sum(output_digits))
