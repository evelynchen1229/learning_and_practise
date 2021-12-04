# for a list of arrays and a list of numbers
# if a number appears in an array, mark the number in the array as -1 (if not the list of numbers)
# if any array has row or column sum as -5, then stop and remember the last bingo number 
# sum all non -1 numbers in that array and multiply by the last bingo number

import numpy as np
new_line = []
bingo_candidates = []
bingo_sets = []

def check_board(board,order):
    for a in board:
        if number in a:
            position = a.tolist().index(number)
            a[position] = -1
    return board

def bingo(board):
    if -5 in array.sum(axis=1) or -5 in array.sum(axis=0):
        return True
    return False

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
def game (boards,order,board_index=0):
    if board_index < len(boards):
        board = boards[board_index]
        updated_board = check_board(board,order)
        board_is_bingoed = bingo(updated_board)
        if board_is_bingoed:
       #     print(num)
            sub_total = residual_sum(update_array)
            bingo_result = num * sub_total
           # print(str(bingo_result).isnumeric())
            #print(board_index,num)
           # print(update_array)
           # print('bingo')
           # print(bingo_result)
            #return bingo_result 
            return board_index

        else:
            boards[board_index] = updated_board
            board_index += 1
            return game(boards,num, board_index)
    else:
        return boards
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
def lst_game(boards):
    num_boards = len(boards)
    bingos=[]
    for order in bingo_candidates:
#        print(num)
        result = game(boards,order)
#        print(result,num)
        some_bingoed = str(result).isnumeric()
        if str(result).isnumeric():
            print(result,num)
            bingos.append(result) #           bingos.append(final_results) array_sets.pop(result)
            
                

    return bingos

last_bingos = lst_game(bingo_sets)
print(last_bingos)
