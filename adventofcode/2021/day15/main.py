from construction import constructor

challenge = constructor('sample.txt')
print(challenge)

'''  def adjacent_nodes(node,graph):
        graph_x,
        graph_y
        node = (x,y)
        right_node = (x+1,y)
        below_node = (x, y+1)
        
        adjacnet_nodes_list = [right_node,below_node]
        adjacent_node_list = [n for n in adjacent_node_list if 0<= x_adjacent <= graph_x and 0<= y_adjacent<= graph_y]


    track previous node, track total cost, if right_node == left_node cost, can do one path then record cost for the "cross road" as current cost. go through the other path and update the current cost if lower.

    keep going until the next move is the end
'''

