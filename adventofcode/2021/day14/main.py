from construction import constructor
from collections import Counter

challenge = constructor('input.txt')
challenge_polymer = challenge['polymer']
challenge_pair = challenge['pair_rule']

insert_letters = [i[-1] for i in challenge_pair]
pairs = [i[0] for i in challenge_pair]

occurance = Counter(insert_letters).most_common()
most_common = occurance[0][0]
least_common = occurance[-1][0]

def dedup(polymer_pair,occurance=[]):
    size = len(polymer_pair)
    pair = []
    agg_occurance = []
    for n in range(0,size):
        p = polymer_pair[n]

        if p not in pair:
            pair.append(p)
            position = pair.index(p)
            if len(occurance) == 0:
                agg_occurance.append(1)
            else:
                occur = occurance[n]
                agg_occurance.append(occur)
        else:
            position = pair.index(p)
            if len(occurance) == 0:
                agg_occurance[position] += 1
            else:
                occur = occurance[n]
                agg_occurance[position] += occur

    pair_occur = {'pair':pair,
            'occurance':agg_occurance
            }
    return pair_occur

def insert_pair(polymer_pair,occurance=[], insert_letter =[],insert_occur=[],insert = insert_letters, insert_pair = pairs):
    dedupping = dedup(polymer_pair,occurance)
    dedupped_pair = dedupping['pair']
    dedupped_occurance = dedupping['occurance']
    new_pairs = []
    new_occur = []
    for p in dedupped_pair:
        index = dedupped_pair.index(p)
        p_occur = dedupped_occurance[index]
        letter_inserted = insert_letters[insert_pair.index(p)]
        # need to find a way without appending repeated pairs
        #for n in range(0,p_occur):
        new_pair_first = p[0] + letter_inserted
        new_pair_second = letter_inserted + p[-1]
        if new_pair_first not in new_pairs:
            new_pairs.append(new_pair_first)
            new_occur.append(p_occur)
        else:
            position = new_pairs.index(new_pair_first)
            new_occur[position] += p_occur

        if new_pair_second not in new_pairs:
            new_pairs.append(new_pair_second)
            new_occur.append(p_occur)
        else:
            position = new_pairs.index(new_pair_second)
            new_occur[position] += p_occur

        if letter_inserted not in insert_letter:
            insert_letter.append(letter_inserted)
            insert_occur.append(p_occur)
        else:
            position = insert_letter.index(letter_inserted)
            insert_occur[position] += p_occur


    insert_dict = {'letters':insert_letter,
                'letters_occur':insert_occur,
                'new_pair':new_pairs,
                'new_occur':new_occur
                }
    return insert_dict


def total_pair(polymer_pair,step=0):
    initial_polymer = ''.join(polymer_pair)
    insert_letter=[]
    insert_occur=[]
    p_size = len(initial_polymer)
    for n in range(0,p_size):
        letter = initial_polymer[n]
        if letter not in insert_letter:
            insert_letter.append(letter)
            insert_occur.append(1)
        else:
            position = insert_letter.index(letter)
            insert_occur[position] += 1
    occurance = []
    for n in range(0,step):
        polymer_insertting = insert_pair(polymer_pair,occurance,insert_letter,insert_occur)
        polymer_pair = polymer_insertting['new_pair']
        occurance = polymer_insertting['new_occur']
        insert_letter = polymer_insertting['letters']
        insert_occur = polymer_insertting['letters_occur']

   #not sure why +1 though
    difference = max(insert_occur)-min(insert_occur) +1

    most_least_occured = {'letters':insert_letter,
            'insert_occur':insert_occur,
            'difference':difference,
            'polymer':polymer_pair,
            'occurance':occurance
            }


    return most_least_occured

def set_up(polymer_template = challenge_polymer):
    size_polymer = len(polymer_template)
    polymer_list = []
    for n in range(0,size_polymer - 1):
        polymer_list.append(polymer_template[n : n + 2])

    return polymer_list

#part1
test = total_pair(set_up(),10) 
print("part1: ",test['difference'])

#part2
test = total_pair(set_up(),40) 
print("part2: ",test['difference'])


