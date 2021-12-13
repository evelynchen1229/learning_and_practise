from construction import constructor
import math

test_syntaxes = constructor('test_input.txt')
challenge_syntaxes = constructor('input.txt')

opening = ['(','{', '[','<']
closing = [')', '}',']','>']


def navigation(syntax_list, position = 0):
    index = opening.index(syntax_list[position])
    legal_closing = closing[index]
    if position + 1 == len(syntax_list):
        return syntax_list
    elif syntax_list[position + 1] == legal_closing:
        del syntax_list[position : position + 2]
        return navigation(syntax_list, position = 0)
    elif syntax_list[position + 1] in closing:
        return syntax_list[position + 1]
    else:
        position += 1
        return navigation(syntax_list, position)

def error_score(syntax, system = 'error'):
    if syntax == ')':
        if system == 'error':
            return 3
        else:
            return 1
    elif syntax == ']':
        if system == 'error':
            return 57
        else:
            return 2
    elif syntax == '}':
        if system == 'error':
            return 1197
        else:
            return 3
    else:
        if system == 'error':
            return 25137
        else:
            return 4

syntax_error_score = 0
for syntax in challenge_syntaxes:
    syntax_error = navigation(syntax)
    if isinstance(syntax_error, list) == False:
        syntax_error_score += error_score(syntax_error)


print("part 1: ", syntax_error_score)


# part 2
autocompletion_scores = []

for syntax in challenge_syntaxes:
    total_score = 0
    syntax_error = navigation(syntax)
    if isinstance(syntax_error, list):
        syntax_error.reverse()
        for s in syntax_error:
            total_score *= 5
            legal_closing = closing[opening.index(s)]
            tool_score = error_score(legal_closing, system = 'autocomplete')
            total_score += tool_score

        autocompletion_scores.append(total_score)

size_scores = len(autocompletion_scores)
medium = math.floor(size_scores / 2)
autocompletion_scores.sort()
medium_score = autocompletion_scores[medium]

print("part 2: ", medium_score)
