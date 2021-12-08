from construction import constructor
import numpy as np
import math

crab_position = constructor('test_input.txt')
max_position = max(crab_position)

size = len(crab_position)
fuel_cost = []
# part 1
#method 1
crab_position.sort()
size = len(crab_position)
medium_location = math.floor(size/2)
medium_crab = crab_position[medium_location]
fuel_cost = 0
for crab in crab_position:
    fuel_cost += abs(crab-medium_crab)

print(fuel_cost)

# method 2
fuel_cost = []
for i in range(0,max_position + 1):
    alignment = []
    alignment.append(i)
    cost = abs(np.array(crab_position) - np.array(alignment * size))
    fuel_cost.append(cost.sum())

least_fuel_cost = min(fuel_cost)
print(least_fuel_cost)

# part 2
fuel_cost = []
for i in range(0,max_position + 1):
    alignment = []
    alignment.append(i)
    cost = abs(np.array(crab_position) - np.array(alignment * size))
    fuel = 0
    for c in cost:
        fuel += (1 + c) * c / 2

    fuel_cost.append(fuel)

least_fuel_cost = min(fuel_cost)
print(least_fuel_cost)
    


