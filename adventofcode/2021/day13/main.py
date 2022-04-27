from construction import constructor
import numpy as np

challenge = constructor('input.txt')
challenge_coordinate = challenge['coordinates']
challenge_fold = challenge['folding']
challenge_max_x = challenge['max_x']
challenge_max_y = challenge['max_y']


max_row = challenge_max_y + 1
max_col = challenge_max_x + 1
paper = np.zeros(shape=(max_row,max_col)) 

def set_up(initial_paper, initial_coordinate):
    for c in initial_coordinate:
        row = c[-1]
        col = c[0]
        initial_paper[row][col] += 1

    return initial_paper 

def folding(folding_line, initial_paper, initial_coordinate ):
    x_fold = folding_line[0]
    y_fold = folding_line[-1]
    paper_x_max = len(initial_paper[0]) - 1
    paper_y_max = len(initial_paper) - 1

    for coordinate in initial_coordinate:
        x = coordinate[0]
        y = coordinate[-1]
        if x <= paper_x_max and y <= paper_y_max:
            if x_fold == 0:
                if y - y_fold > 0:
                    coordinate[-1] = 2 * y_fold - y
                    new_y = coordinate[-1]
                    if marked_paper[new_y][x] == 0:
                        marked_paper[new_y][x] += 1
            else:
                if x- x_fold > 0:
                    coordinate[0] = 2 * x_fold - x
                    new_x = coordinate[0]
                    if marked_paper[y][new_x] == 0:
                        marked_paper[y][new_x] += 1
    
    if x_fold == 0:
        folded_paper = marked_paper[:y_fold]
        num_dots = np.count_nonzero(folded_paper == 1)
    else:
        folded_paper = marked_paper[:,:x_fold]
        num_dots = np.count_nonzero(folded_paper == 1)

    folded = {'folded_paper':folded_paper,
            'num_of_dots':num_dots
            }
    return folded


marked_paper = set_up(paper,challenge_coordinate)

# part 1
part1 = folding(challenge_fold[0], marked_paper,challenge_coordinate)
print("part1:",part1['num_of_dots'])

# part 2

num_of_dots = 0
for folding_line in challenge_fold:
    folded = folding(folding_line, marked_paper,challenge_coordinate)
    marked_paper = folded['folded_paper']
    num_of_dots += folded['num_of_dots']

size = len(marked_paper)

code_paper = np.where(marked_paper==0,'.',marked_paper)
code_paper = np.where(code_paper=='1.0','#',code_paper)
for i in range(0,size):
    print(code_paper[i])

print("part 2: CEJKLUGJ")




    

