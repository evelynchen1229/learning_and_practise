'''human player == 1'''
#import random

def robot_move(remain_tile):

    for n in range(1, 4 ,1):
        if (remain_tile - n) % 4 == 0:
            return n

def sticks_game(tiles_left):

    #while tiles_left in range (4 , 21):
    while tiles_left > 0:
        player_move = int(input("Please type how many tiles you want to take (1 - 3): "))
        tiles_left -= player_move
        print(f"tiles_left now is {tiles_left}")
        if tiles_left == 0: # not gonna happen mate
            print(f"Oh my! Blind me! You won the game!")
            return
        computer_move = robot_move(tiles_left)
        print(f"Robot's move: {computer_move}")
        tiles_left -= computer_move
        print(f"tiles_left now is {tiles_left}")

        return sticks_game(tiles_left)

    print(f"Computer won as it takes all the remaining tiles")
    return tiles_left



initial_tile = 21
robot_first_move = 1

print(f"Robot's first move: {robot_first_move}")
first_round = initial_tile - robot_first_move
print(first_round)
sticks_game(first_round)





