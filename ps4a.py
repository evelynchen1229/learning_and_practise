# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''
    permutation_list = []
    if len(sequence)==1:
        permutation_list.append(sequence)
        #print(permutation_list)
        return permutation_list
    else:
        remaining = sequence[1:]
        first_char = sequence[0]
       # print(first_char)
       # print(remaining)
        start_list = get_permutations(remaining)
        for per in start_list:
            #print(per)
            str_len = 1+len(per)
            for n in range(0,str_len):
                #insert first_char to all possible positions
                if n ==0:
                    new_word=first_char+per
                #    print(new_word)
                elif n <str_len-1:
                    new_word=per[0:n]+first_char+per[n:]
                #    print(new_word)
                else:
                    new_word=per+first_char
                #    print(new_word)

                if new_word not in permutation_list:
                    permutation_list.append(new_word)
                #print(permutation_list)
#        print(permutation_list)
        return(permutation_list)




if __name__ == '__main__':
#    #EXAMPLE
    example_input = 'abcde'
    print('Input:', example_input)
    #print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    final_list=get_permutations(example_input)
    element = len(final_list)
    print('Actual Output:',final_list )
    print('Elements: ',element)

#    # Put three example test cases here (for your sanity, limit your inputs
#    to be three characters or fewer as you will have n! permutations for a
#    sequence of length n)


