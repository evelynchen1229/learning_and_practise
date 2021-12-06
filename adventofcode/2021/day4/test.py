import numpy as np
bingo_sets = []
scores = []
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
            # remove the bingoed board from the game
            boards.pop(board_index)
        else:
            pass

        board_index += 1
        return game(boards,order,board_index)

    board_score_dict = {'boards':boards,
            'score':scores
            }

    return board_score_dict

def bingo_game(boards,orders_index = 0):
    final_scores = []
    num_orders = len(bingo_candidates)
    if orders_index < num_orders:
        order = bingo_candidates[orders_index]
        print(order)
        order_result = game(boards,order)

        boards = order_result['boards']
        print(boards)
        final_scores.append(order_result['score'])
        print(final_scores)
        orders_index += 1
        if len(boards) > 0:
            return bingo_game(boards,orders_index)
        return final_scores
    return final_scores


array_4 = np.array([[1000,24,2,145,4],
    [2,3,4,5,1],
    [21,22,23,24,25],
    [2,5,334,12,41],
    [2,25,24,15,166]
    ],dtype=object)
print(bingo_sets[0])
is_in_list = np.all(np.all(array_2 == bingo_sets,axis=1))
mask = np.isin(array_2,bingo_sets)
print(mask)
print (False in mask)
