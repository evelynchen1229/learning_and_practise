from construction import constructor
#initial_state = constructor('test_input.txt')
initial_state = constructor('input.txt')

def number_of_fish(state,days):
    previous_state = {'0':state.count(0),
                '1': state.count(1),
                '2': state.count(2),
                '3': state.count(3),
                '4': state.count(4),
                '5': state.count(5),
                '6': state.count(6),
                '7': state.count(7),
                '8': state.count(8)
                }


    for day in range(0,days):
        initial_0 = previous_state['0']
        previous_state['0'] = previous_state['1']
        previous_state['1'] = previous_state['2']
        previous_state['2'] = previous_state['3']
        previous_state['3'] = previous_state['4']
        previous_state['4'] = previous_state['5']
        previous_state['5'] = previous_state['6']
        previous_state['6'] = initial_0 + previous_state['7']
        previous_state['7'] = previous_state['8']
        previous_state['8'] = initial_0

    total_fish = sum(previous_state.values())
    return total_fish 
# part 1
fish_volume = number_of_fish(initial_state,80)
print(fish_volume)

# part 2

huge_number_of_fish = number_of_fish(initial_state,256)
print(huge_number_of_fish)

print('hello Rossella')
