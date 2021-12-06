import math

from construction import constructor
initial_state = constructor('test_input.txt')
#initial_state = constructor('input.txt')
#print(initial_state)

# part 1
def number_of_fish(state,days):
    num_of_fish = len(state)
    if days > 0:
        days -= 1
        for fish_number in range(0,num_of_fish):
            fish = state[fish_number]
            if fish == 0:
                state[fish_number] = 6
                state.append(8)
            else:
                state[fish_number] -= 1

        return number_of_fish(state,days)

    return state

test = number_of_fish([3],18)
#print(test)
total_number_of_fish = len(test)
print(total_number_of_fish)


def synced_fish(state):
    synced = []
    for i in range(0,7):
        synced.append(state.count(i))
    return synced

test = synced_fish(initial_state) 
print(test)


def num_of_fish_created(fish,days):
    if fish >= days:
        return 0
    else:
        cycles = math.ceil((days - fish) / 7)
    return cycles

def num_of_fish_can_reproduce(fish,days):
    if fish >= days:
        return 0
    else:
        full_cycles = math.floor((days - fish) / 7)
    return full_cycles

def total_fish(fish,days):
    # get total number of fish produced by the first fish
    num_fish_created = num_of_fish_created(fish,days)
    if num_fish_created == 0:
        return 1 # initial fish
    else:
        for num_fish in range(0,num_fish_created):
            #days_before_cycle
            fish += num_fish * 7 + 2 + 7
            #find how many fish being created by each fish created by the first fish
            fish_created = num_of_fish_created(fish, days)
            if fish_created == 0:
                num_fish_created += 1
                return num_fish_created
            else:
                num_fish_created += fish_created
                # find how many of the fish created can actually have time to reproduce
                fish_can_reproduce = num_of_fish_can_reproduce(fish,days)
                if fish_can_reproduce == 0:
                    total_fish = 1 + num_fish_created # add the initial fish
                    return total_fish
                else:
                # repeat the procedure
                       pass

test = total_fish(1,15)
print(test)



            



