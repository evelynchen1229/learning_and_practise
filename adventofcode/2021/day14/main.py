from construction import constructor
from collections import Counter

challenge = constructor('input.txt')
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
