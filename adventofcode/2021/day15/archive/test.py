from construction import constructor

challenge = constructor('sample.txt')

challenge_cost = challenge['values']
challenge_graph = challenge['position']

start_node = [0,0]
target_node = max(challenge['position'])
target_cost = challenge_cost[target_node[1]][target_node[0]]

''' 

    track previous node, track total cost, if right_node == left_node cost, can do one path then record cost for the "cross road" as current cost. go through the other path and update the current cost if lower.

    keep going until the next move is the end
'''

def adjacent_node(node, graph_pos = challenge_graph, graph_value = challenge_cost):
    max_x = len(graph_value[0])
    max_y = len(graph_value)

    x_node = node[0]
    y_node = node[1]

    right_node = [x_node + 1, y_node]
    below_node = [x_node, y_node + 1]

    adjacent_node_list = [right_node, below_node]
    legal_adjacent_node = [n for n in adjacent_node_list if 0 <= n[0] < max_x and 0 <= n[1] < max_y]

    right_node_position = legal_adjacent_node [0]
    right_node_value = graph_value[right_node_position[1]][right_node_position[0]]

    below_node_position = legal_adjacent_node[-1]
    below_node_value = graph_value[below_node_position[1]][below_node_position[0]]

    adjacent_nodes = {'right_node' : right_node_position,
            'right_node_cost' : right_node_value,
            'below_node' : below_node_position,
            'below_node_cost' : below_node_value
            }

    return adjacent_nodes

def reach_target(node):
    adjacents = adjacent_node(node)

    if target_node in [adjacents['right_node'],adjacents['below_node']]:
        return True
    else:
        return False


def next_node(starting_node = start_node, previous_node = [start_node], current_cost = 0, graph = challenge_graph):
    if reach_target(starting_node) == True:
        print("reaching target")
        current_cost += target_cost
        least_route = {'previous_node': previous_node,
           'total_cost' : current_cost
           }
        return least_route
    else:
        adjacents = adjacent_node(starting_node)
        if adjacents['right_node_cost'] < adjacents['below_node_cost']:
            current_cost += adjacents['right_node_cost']
            previous_node.append(adjacents['right_node'])
            starting_node = adjacents['right_node']
            least_route = next_node(starting_node, previous_node, current_cost)
        elif adjacents['right_node_cost'] > adjacents['below_node_cost']:
            current_cost += adjacents['below_node_cost']
            previous_node.append(adjacents['below_node'])
            starting_node = adjacents['below_node']
            least_route = next_node(starting_node, previous_node, current_cost)
        elif adjacents['right_node'] == adjacents['below_node']:
            current_cost += adjacents['below_node_cost']
            previous_node.append(adjacents['below_node'])
            starting_node = adjacents['below_node']
            least_route = next_node(starting_node, previous_node, current_cost)
        else:
            current_cost += adjacents['right_node_cost']
            right_node_case = next_node(adjacents['right_node'], previous_node, current_cost)
            right_node_total_cost = right_node_case['total_cost']
            right_node_ending_position = right_node_case['previous_node'] 
            previous_node = previous_node[:-1]

            below_node_case = next_node(adjacents['below_node'], previous_node,current_cost )
            below_node_total_cost = below_node_case['total_cost']
            below_node_ending_position = below_node_case['previous_node']
            print("right",right_node_total_cost,"below",below_node_total_cost)

            if right_node_total_cost > below_node_total_cost:
                print("going below")
                print(previous_node)
                print(below_node_total_cost)
                print(current_cost)
                current_cost = below_node_total_cost
                previous_node = below_node_ending_position
                starting_node = previous_node[-1]
                least_route = {'previous_node': previous_node,
                   'total_cost' : current_cost
                   }
            else:
                print("going right")
                print(previous_node)
                current_cost = right_node_total_cost
                previous_node = right_node_ending_position
                starting_node = previous_node[-1]
                least_route = {'previous_node': previous_node,
                   'total_cost' : current_cost
                   }

            #least_route = next_node(starting_node, previous_node, current_cost)
        #print(least_route)

   

    return least_route 

print(next_node([0,0]))



#adjacent_node = adjacent_nodes(pos,challenge_graph)
#if adjacent_node[0] == adjacent_node[1]:
#    x = adjacent_node[0][0]
#    y = adjacent_node[0][1]
#    current_cost += challenge_cost[y][x]
#    visited.append(pos)
#    previous_node.append(pos)
#    next_cost = []
#    for adj in adjacent_node:
#        # repeat
#        next_cost.append(cost)
#    if next_cost[0] < next_cost[1]:
#        current_cost += next_cost[0]
#        previous_node.append(adjacent pos related with next_cost[0]
#    else:
#        current_cost += next_cost[1]
#        previous_node.append(adjacent pos related with next_cost[1]
#elif left > below:
#    current_cost += left_value
#    previous.append(left_position)
#else:
#    current_cost += below_value
#    previous.append(below_position)
