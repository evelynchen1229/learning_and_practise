import numpy as np
def update_number(array,number):
    for a in array:
        if number in a:
            position = a.tolist().index(number)
            a[position] = -1
        else:
            pass
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
bingo_sets = []
array_1 = np.array([[2,3,4,1,9],
    [5,6,7,3,9],
    [1,2,3,4,5],
    [11,12,13,14,15],
    [11,14,15,67,2]
    ],dtype=object
    )
#for a in array_1:
#    if 2 in a:
#        print(a)
#        for i in a:
#            if i == 2:
#                positon = a.tolist().index(i)
#                print(positon)
array_2 = np.array([[1,2,3,20,32],
    [5,6,7,42,51],
    [3,4,5,1,121],
    [2,4,5,6,3],
    [10,9,8,7,6]
    ],dtype=object)

array_3 = np.array([[0,24,2,145,4],
    [2,3,4,5,1],
    [21,22,23,24,25],
    [2,5,334,12,41],
    [2,25,24,15,166]
    ],dtype=object)
for array in (array_1, array_2, array_3):
    bingo_sets.append(array)
bingo_candidates = [2,3,4,5,6]
for num in bingo_candidates:
    for set_number in range(0,3):
        updated_bingo_set = update_number(bingo_sets[set_number],num)
        print(updated_bingo_set)
        result = bingo(updated_bingo_set)
        print(result)
        bingo_sets[set_number] = updated_bingo_set
        print(bingo_sets)
        if result != 'bingo':
            pass
        else:
            break

sub_total = residual_sum(updated_bingo_set)
bingo_result = num * sub_total
print(num,set_number,sub_total,bingo_result)
bingo_sets.pop(0)
print(bingo_sets)
