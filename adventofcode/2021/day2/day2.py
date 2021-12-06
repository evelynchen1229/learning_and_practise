def movement(instruction):
    move = int(instruction[-1])
    return move

instructions = []
horizontal = 0
vertical = 0

with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        instructions.append(line)
f.close()

# part 1
horizontal = 0
vertical = 0

for i in instructions:
    if i[0] == 'f':
        horizontal += movement(i)
    elif i[0] == 'u':
        vertical -= movement(i)
    else:
        vertical += movement(i)

position = horizontal * vertical
print(position)

# part 2
horizontal = 0
aim = 0
depth = 0

for i in instructions:
    if i[0] == 'f':
        horizontal += movement(i)
        depth += aim * movement(i)
    elif i[0] == 'u':
        aim -= movement(i)
    else:
        aim += movement(i)

position = horizontal * depth
print(position)
