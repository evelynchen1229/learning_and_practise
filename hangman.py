# Problem Set 2, hangman.py
# Name:
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words_hangman.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
#    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
#    print(len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)
    pass

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    #secret_letters = secret_word.split()
    #returns ['apple']
    secret_letters = list(secret_word)
    guessed = 0
    for i in secret_letters:
        if i in letters_guessed:
            guessed += 1
        else:
            pass
    print(guessed == len(secret_letters))
    return letters_guessed

    pass

#guessing_word = input("guess a word please: ").lower()
##assert guessing_word.islower(), 'please put lower case word'
#
#is_guessed = list(guessing_word)
#is_guessing = is_word_guessed('apple',is_guessed)


def get_guessed_word(secret_word, letters_guessed=''):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    secret_letters = list(secret_word)
    #print(secret_letters)
    guessed_letters = []
    if len(letters_guessed) >0:
        for i in secret_letters:
            if i in letters_guessed:
                guessed_letters.append(i)
            else:
                guessed_letters.append('_')
        result ="".join(guessed_letters)
    else:
        result = '-'*len(secret_word)
#    print(result)
    return result
 #   pass
#guessing_word = input("guess a word please: ").lower()
##assert guessing_word.islower(), 'please put lower case word'
#guessed_word = list(guessing_word)
#guessing_word = get_guessed_word('apple',guessed_word)




def get_available_letters(letters_guessed=''):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    full_letters = string.ascii_lowercase
    full_lowercase_list = list(string.ascii_lowercase)
    all_available_letters = []
    if len(letters_guessed)>0:

        for i in full_lowercase_list:
            if i in letters_guessed:
                pass
            else:
                all_available_letters.append(i)

        result = "".join(all_available_letters)
    else:
        result = full_letters
    #print(result)
    return result

#guessing_word = input("guess a word please: ").lower()
#assert guessing_word.islower(), 'please put lower case word'
##guessed_available = list(guessing_word)

#available_letters = get_available_letters(guessed_available)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    #Bugs to be sloved
    '''
    1. dynamic available letters (not including the guessed ones atm) # done
    2.dynamic word_now (one letter being shown only atm) # done
    3.
    '''
    secrect_len = len(secret_word)
    warnings = 3
    guessing_round = 6
    deducting = 0
    print('''Welcom to the game Hangman!\nI am thinking of a word that is {0} letters long.\nYou have {1} warnings left.\n---------------------------'''.format(secrect_len,warnings))
    guessed_list = []
    correct_guess_list = []
    all_available_letters = string.ascii_lowercase

    print('''You have {0} guesses left.\nAvailable letters: {1}
    '''.format(guessing_round,all_available_letters))
    word_now =''
    while guessing_round >0 :
        if word_now == secret_word:
            break

        letter_guessed = input("Please guess a letter: ")


        if letter_guessed.isalpha():

            if letter_guessed in guessed_list:
                if warnings == 0:
                    guessing_round -= 1
                    print('''You've guessed this letter already.\nYou don't have
                            any more warnings chances.\n------------------''')
                else:
                    warnings -= 1
                print("Oops! You've already guessed this letter. You have {0} warnings left:{1}\n------------------".format(warnings,word_now))
            elif letter_guessed in secret_word :
                guessed_list.append(letter_guessed)
                already_guessed = ''.join(guessed_list)
                available_letters = get_available_letters(already_guessed)

                correct_guess_list.append(letter_guessed)
                correct_guess=''.join(correct_guess_list)
                word_now = get_guessed_word(secret_word, correct_guess)
                print("Good guess: ",word_now, "\n------------------")
            elif letter_guessed not in secret_word and letter_guessed in 'aeiou':
                guessed_list.append(letter_guessed)
                already_guessed = ''.join(guessed_list)
                available_letters = get_available_letters(already_guessed)
                word_now = get_guessed_word(secret_word, correct_guess)
                guessing_round -=2
                print("Oops! That letter is not in my word: {}\n------------------".format(word_now))
            else:
                guessed_list.append(letter_guessed)
                already_guessed = ''.join(guessed_list)
                available_letters = get_available_letters(already_guessed)
                word_now = get_guessed_word(secret_word, correct_guess)
                guessing_round -= 1
                print("Oops! That letter is not in my word: {}\n------------------".format(word_now))

        elif warnings == 0:
            guessing_round -= 1
            print("Oops! That is not a valid letter. You have no warnings left.\n------------------")
        else:
            warnings -= 1
            print("Oops! That is not a valid letter. You have {0} warnings left: {1}\n------------------".format(warnings,word_now))

        print('''You have {0} guesses left.\nAvailable letters: {1}
        '''.format(guessing_round,available_letters)
        )
    if word_now == secret_word:
        score = guessing_round * len(secret_word)
        print("Congratulations, you won!\nYour total score for this game is: {}".format(score))
        return word_now
    else:
        print("Sorry, you ran out of guesses. The word was else")
        return word_now



    # FILL IN YOUR CODE HERE AND DELETE "pass"
    pass
#test = hangman('apple')


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
   # secret_guess = 'apple'
    #my_word = get_guessed_word(secret_word, my_guess)
    result=[]
    if len(my_word.strip())==len(other_word.strip()):
        for i in my_word:
            location = my_word.index(i)
            if i != '_' and other_word[location]==i:
                result.append('1')
            elif i == '_':
                pass
            else:
                result.append('0')
    else:
        return 'False'
    if '0' in result:
        return 'False'
    else:
        return 'True'


    pass




def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    #pass
    candidate_words =load_words()
    potential_words = []

    for word in candidate_words:
        check = match_with_gaps(my_word,word)
        if check == 'True':
            potential_words.append(word)

    if len(potential_words)==0:
        print("No matches found")
    else:
        match = ' '.join(potential_words)
        print(match)

    return 0

#show_possible_matches('att___')




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    # FILL IN YOUR CODE HERE AND DELETE "pass"
    secrect_len = len(secret_word)
    warnings = 3
    guessing_round = 6
    print('''Welcom to the game Hangman!\nI am thinking of a word that is {0} letters long.\nYou have {1} warnings left.\n---------------------------'''.format(secrect_len,warnings))
    guessed_list = []
    correct_guess_list = []
    all_available_letters = string.ascii_lowercase

    print('''You have {0} guesses left.\nAvailable letters: {1}
    '''.format(guessing_round,all_available_letters))
    word_now =''
    while guessing_round >0 :
        if word_now == secret_word:
            break

        letter_guessed = input("Please guess a letter: ")


        if letter_guessed.isalpha() or letter_guessed == '*':

            if letter_guessed in guessed_list:
                if warnings == 0:
                    guessing_round -= 1
                    print('''You've guessed this letter already.\nYou don't have
                            any more warnings chances.\n------------------''')
                else:
                    warnings -= 1
                print("Oops! You've already guessed this letter. You have {0} warnings left:{1}\n------------------".format(warnings,word_now))
            elif letter_guessed == '*':
                if word_now=='':
                    really = input("Are you sure to have all 55,900 words showing on the screen?:y/n ")
                    if really=='n':
                        available_letters=string.ascii_lowercase
                    else:
                        available_letters=string.ascii_lowercase
                        print (load_words())
                else:
                    print(word_now)
                    show_possible_matches(word_now)

            elif letter_guessed in secret_word :
                guessed_list.append(letter_guessed)
                already_guessed = ''.join(guessed_list)
                available_letters = get_available_letters(already_guessed)

                correct_guess_list.append(letter_guessed)
                correct_guess=''.join(correct_guess_list)
                word_now = get_guessed_word(secret_word, correct_guess)
                print("Good guess: ",word_now, "\n------------------")
            elif letter_guessed not in secret_word and letter_guessed in 'aeiou':
                guessed_list.append(letter_guessed)
                already_guessed = ''.join(guessed_list)
                available_letters = get_available_letters(already_guessed)
                if len(correct_guess_list)==0:
                    word_now=get_guessed_word(secret_word,'')
                else:
                    word_now = get_guessed_word(secret_word, correct_guess)
                guessing_round -=2
                print("Oops! That letter is not in my word: {}\n------------------".format(word_now))
            else:
                guessed_list.append(letter_guessed)
                already_guessed = ''.join(guessed_list)
                available_letters = get_available_letters(already_guessed)
                if len(correct_guess_list)==0:
                    word_now=get_guessed_word(secret_word,'')
                else:
                    word_now = get_guessed_word(secret_word, correct_guess)
                guessing_round -= 1
                print("Oops! That letter is not in my word: {}\n------------------".format(word_now))

        elif warnings == 0:
            guessing_round -= 1
            print("Oops! That is not a valid letter. You have no warnings left.\n------------------")
        else:
            warnings -= 1
            print("Oops! That is not a valid letter. You have {0} warnings left: {1}\n------------------".format(warnings,word_now))

        print('''You have {0} guesses left.\nAvailable letters: {1}
        '''.format(guessing_round,available_letters)
        )
    if word_now == secret_word:
        score = guessing_round * len(secret_word)
        print("Congratulations, you won!\nYour total score for this game is: {}".format(score))
        return word_now
    else:
       print("Sorry, you ran out of guesses. The word was else: ",secret_word)
       return word_now
    #pass

secret_word = choose_word(wordlist)
#secret_word='boots'
hangman_with_hints(secret_word)


# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


#if __name__ == "__main__":
#    # pass
#
#    # To test part 2, comment out the pass line above and
#    # uncomment the following two lines.
#
#    secret_word = choose_word(wordlist)
#    hangman(secret_word)
#
###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    #secret_word = choose_word(wordlist)
    #hangman_with_hints(secret_word)
