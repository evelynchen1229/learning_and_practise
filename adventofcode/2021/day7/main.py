from construction import constructor
import numpy as np

crab_position = constructor('input.txt')
max_position = max(crab_position)

size = len(crab_position)
fuel_cost = []
# part 1
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
    


