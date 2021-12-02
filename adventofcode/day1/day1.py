def integer(i):
    integer = int(i.strip())
    return integer

def sub_total(item):
    num = 1
    total = 0
    if num <= 3:
        total += item
        num +=1
    return total


with open ('input.txt') as f:
    lines = f.readlines()
    length = len(lines)
    count = 0
    for i in range(1,length):
        if integer(lines[i]) > integer(lines[i-1]):
            count += 1

print(count)

total_sum = []
num = 1

for i in range(0,length):
    if num <= 3:
        sub_total(integer(lines[i])
        total = 0
        if num <=3:
            total += integer(lines[i])
            num +=1
        else:
            total_sum.append(total)

