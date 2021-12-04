# for a list of arrays and a list of numbers
# if a number appears in an array, mark the number in the array as -1 (if not the list of numbers)
# if any array has row or column sum as -5, then stop and remember the last bingo number 
# sum all non -1 numbers in that array and multiply by the last bingo number

import numpy as np
new_line = []
bingo_candidates = []
bingo_sets = []

def update_number(array,number):
    for a in array:
        if number in a:
            position = a.tolist().index(number)
            a[position] = -1
    return array

def bingo(array):
    if -5 in array.sum(axis=1) or -5 in array.sum(axis=0):
        return 'bingo'
    else:
        pass

def residual_sum(array):
    total = array.sum()
    mask = np.where(-1)
    for row in array:
        if -1 in row:
            for element in row:
                if element == -1:
                    total += 1
    return total
            

with open('input.txt') as f:
    lines = f.readlines()
    bingo_numbers = lines[0].strip().split(',')
    for i in bingo_numbers:
        i = int(i)
        bingo_candidates.append(i)

    for line in lines[1:]:
        if len(line) == 1 and '' in line:
            pass
        else:
            num_list = []
            line = line.strip().split(' ')
            for i in line:
                if i != '':
                    i = int(i)
                    num_list.append(i)
            new_line.append(num_list)
f.close()

num_sets = int(len(new_line)/5)

candidates = len(bingo_candidates)

for i in range(1,num_sets + 1):
    bingo_set = np.array(new_line[(i-1)*5 : i*5])
    bingo_sets.append(bingo_set)

# part 1
def game (array_sets,num,set_number=0):
    if set_number < len(array_sets):
        array = array_sets[set_number]
        update_array = update_number(array,num)
        result = bingo(update_array)
        if result == 'bingo':
       #     print(num)
            sub_total = residual_sum(update_array)
            bingo_result = num * sub_total
           # print(str(bingo_result).isnumeric())
            #print(set_number,num)
           # print(update_array)
           # print('bingo')
           # print(bingo_result)
            #return bingo_result 
            return set_number

        else:
            array_sets[set_number] = update_array
            set_number += 1
            return game(array_sets,num, set_number)
    else:
        return array_sets
# not working as expected
#def game_set(array_sets,numbers=0):
#    if numbers < candidates:
#        num = bingo_candidates[numbers]
#        game_result = game(array_sets,num, set_number = 0)
#        if str(game_result).isnumeric():
##            print(array_sets,num)
#            return game_result
#        else:
#            numbers += 1
#            array_sets = game_result
# #           print(array_sets)
#            return game_set(array_sets,numbers)
#    else:
#        return 'no bingo'
#correct answer
#bingo_sets.pop(37)
#bingo_sets.pop(45)
#bingo_sets.pop(1)
#bingo_sets.pop(24)
#bingo_sets.pop(75)
#bingo_sets.pop(10)
#bingo_sets.pop(23)
#bingo_sets.pop(58)
#bingo_sets.pop(70)
#bingo_sets.pop(3)
#bingo_sets.pop(9)
#bingo_sets.pop(78)
#bingo_sets.pop(20)
#bingo_sets.pop(41)
#bingo_sets.pop(16)
#bingo_sets.pop(26)
##for num in bingo_candidates:
#    result = game(bingo_sets,num)
#    if str(result).isnumeric():
#        
#        print(result,num)
#        break


# part 2
#print(len(bingo_candidates))
def lst_game(array_sets):
    number_sets = len(array_sets)
    bingos=[]
    for num in bingo_candidates:
#        print(num)
        result = game(array_sets,num)
#        print(result,num)
        if str(result).isnumeric():
            print(result,num)
            bingos.append(result)
 #           bingos.append(final_results)
            array_sets.pop(result)
            
                

    return bingos
last_bingos = lst_game(bingo_sets)

print(last_bingos)
