import math

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

def comparison(item_list):
    list_length = len(item_list)
    count = 0
    for i in range(1,list_length):
        if item_list[i] > item_list[i-1]:
            count += 1
    return count


numbers = []
with open ('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        line = integer(line)
        numbers.append(line)
f.close()

length = len(numbers)

# part 1 - how many numbers are bigger than the previous one
number_compare = comparison(numbers)
print(number_compare)

## part 2 - every next 3 numbers are a group, how many group sum is bigger than the previous group
totals = []
for i in range(0,length-2):
    next_three = numbers[i:i+3]
    total = sum(next_three)
    totals.append(total)


sum_compare = comparison(totals)
print(sum_compare)
