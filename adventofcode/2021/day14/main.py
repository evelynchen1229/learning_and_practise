from construction import constructor
from collections import Counter

challenge = constructor('sample.txt')
challenge_polymer = challenge['polymer']
challenge_pair = challenge['pair_rule']

def inserting(polymer_template, pair_rule = challenge_pair):
    polymer_size = len(polymer_template)
    process = []
    for i in range(0,polymer_size-1):
        pair = polymer_template[i:i+2]
        process.append(pair)
    last_item = process[-1]
    process_size = len(process)

    for n in range(0,process_size - 1):
        value = process[n]
        for r in pair_rule:
            if value in r:
                if process[n][-1] == process[n+1][0]:
                    process[n] = value[0] + r[-1]
                else:
                    process[n] = value[0] + r[-1] + value[-1]
    process = process[:-1]
    for r in pair_rule:
        if last_item in r:
            last_item = last_item[0] + r[-1] + last_item[-1]
            process.append(last_item)

    polymer_template = ''.join(process)

    return polymer_template

def polymerization(polymer_template,step=0,pair_rule =challenge_pair):
    for i in range(0,step):
        polymer_template = inserting(polymer_template)

    return polymer_template

# part 1
challenge = polymerization(challenge_polymer,10)

occurance = Counter(challenge).most_common()
difference = occurance[0][-1] - occurance[-1][-1]
print("part 1: ",difference)


# part 2

pair_replace = []
for p in challenge_pair:
    replacement = p[0][0]+p[-1]+p[0][-1]
    pair_replace.append([p[0],replacement])
def polymer_pair(polymer_template , pair_replacement = pair_replace):
    polymer_list = []
    polymer_size = len(polymer_template)
    for n in range(0,polymer_size - 1):
        polymer_list.append(polymer_template[n: n+2])
    
    polymer_list_size = len(polymer_list)
    for p in pair_replacement:
        for n in range(0,polymer_list_size):
            value = polymer_list[n]
            if p[0] == value:
                polymer_list[n] = p[-1]
    for n in range(0,polymer_list_size - 1):
        value = polymer_list[n]
        if value[-1] == polymer_list[n+1][0]:
            polymer_list[n] = value[:-1]
    polymer_template = ''.join(polymer_list)

    return polymer_template 

def part2_polymerization(polymer_template,step=0,pair_replacement=pair_replace):
    for i in range(0,step):
        polymer_template = polymer_pair(polymer_template)

    return polymer_template
test = part2_polymerization(challenge_polymer,40)
print(len(test))
occurance = Counter(test).most_common()
difference = occurance[0][-1] - occurance[-1][-1]
print("part 2: ",difference)
