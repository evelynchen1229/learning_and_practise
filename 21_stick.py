'''human player == 1'''
import random

def robot_move (remain_tile):

    for n in range (1, 4 ,1):
        if (remain_tile - n) % 4 == 0:
            return n

def sticks_game (tiles_left):

    while tiles_left in range (4 , 21):

        player_move = int(input("Please type how many tiles you want to take (1 - 3): "))
        tiles_left -= player_move
        print(f"tiles_left now is {tiles_left}")
        computer_move =  robot_move (tiles_left)
        print(f"Robot's move: {computer_move}")
        tiles_left -= computer_move
        print(f"tiles_left now is {tiles_left}")

        return sticks_game(tiles_left)

    print(f"Computer won as it takes all the remaining tiles")
    return tiles_left



initial_tile = 21
first_move = random.randrange(1,3,1)
print(f"Robot's first move: {first_move}")
first_round = initial_tile -first_move
print(first_round)

sticks_game(first_round)





        #tiles_left -= computer_move
        #tiles_left = 18 -2 =16


#print(initial)

#tile = 21

#players = input("Please type the number of human players: ")

#players = 2
#rounds = 1








