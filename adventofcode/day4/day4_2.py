import numpy as np
'''list of numbers for bingos'''
orders= []
'''array of bingo boards'''
initial_boards = []
'''array of bingoed boards'''
bingoed_boards = []
'''list of bingoed scores'''
scores = []

# step 1: constract the list of bingo numbers and array of bingo boards
with open('input.txt') as f:
    lines = f.readlines()
    bingo_numbers = lines[0].strip().split(',')
    for i in bingo_numbers:
        i = int(i)
        orders.append(i)

    new_line = []

    for line in lines[1:]:
        if len(line) == 1 and '' in line:
            pass
        else:
            numeric_lines = []
            line = line.strip().split(' ')
            for i in line:
                if i != '':
                    i = int(i)
                    numeric_lines.append(i)
            new_line.append(numeric_lines)
f.close()

num_boards = int(len(new_line)/5)

num_orders = len(orders)

for i in range(1,num_boards + 1):
    board = np.array(new_line[(i-1)*5 : i*5])
    initial_boards.append(board)

# step 2: mark boards when a number is called
def check_board(board,order):
    for b in board:
        if order in b:
            location = b.tolist().index(order)
            b[location] = -1
    return board

def bingo(board):
    if -5 in board.sum(axis=1) or -5 in board.sum(axis=0):
        return True
    return False

def unmarked_sum(board):
    unmarked = 0
    for row in board:
        for number in row:
            if number != -1:
                unmarked += number
    return unmarked

def game(boards,order,board_index = 0):
    number_of_boards = len(boards)
    if board_index < number_of_boards:
        # fetch the board
        board = boards[board_index]
        # check whether the order is in the board; if so mark it
        checked_board = check_board(board,order)
        # update the set of boards by replacing the original board with the marked board
        boards[board_index] = checked_board
        # check if there is a bingo
        board_is_bingoed = bingo(checked_board)

        if board_is_bingoed:
            # caculate score
            score = order * unmarked_sum(checked_board)
            # put score in the collection
            scores.append(score)
            # collect the bingoed board from the game
            bingoed_boards.append(boards)
        else:
            pass

        board_index += 1
        return game(boards,order,board_index)
    # remove bingoed boards from the game
    for bingoed_board in bingoed_boards:


    board_score_dict = {'boards':boards,
            'score':scores
            }

    return board_score_dict

def bingo_game(boards,orders_index = 0):
    final_scores = []
    if orders_index < num_orders:
        order = orders[orders_index]
        order_result = game(boards,order)
        boards = order_result['boards']
        final_scores.append(order_result['score'])
        orders_index += 1
        if len(boards) > 0:
            return bingo_game(boards,orders_index)
        return final_scores
    return final_scores

test = bingo_game(initial_boards)[0]
print(test[0],test[-1])









