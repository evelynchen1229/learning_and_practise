# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : <your name>
# Collaborators : <your collaborators>
# Time spent    : <total time>

import math
import random
import string

VOWELS = 'aeiou'
VOWELS_blank = 'aeiou*'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,'*':0}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words_ps3.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """

#    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
#    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """

    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq


# (end of helper code)
# -----------------------------------

#
# Problem #1: Scoring a word
#
def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters,
    or the empty string "". You may not assume that the string will only contain
    lowercase letters, so you will have to handle uppercase and mixed case strings
    appropriately.

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """

    #pass  # TO DO... Remove this line when you implement this function
    """prepare scrabble word list - .keys()
    scrabble word score list - .values()
    """
   # scrabble_word =[]
   # for w in SCRABBLE_LETTER_VALUES.keys():
   #     scrabble_word.append(w)
   # scrabble_score =[]
   # for s in SCRABBLE_LETTER_VALUES.values():
   #     scrabble_score.append(s)
    first_part = 0
    for i in word.lower():

   #     position = scrabble_word.index(i)
   #     score = scrabble_score[position]
        score=SCRABBLE_LETTER_VALUES[i]

        first_part += score
#    print("first_part score: ",first_part)

    second_part = max(7 * len(word)-3 * (n-len(word)),1)
 #   print(second_part)
    if word=="":
       word_score=0
    else:
       word_score = first_part * second_part
  #  print("total word_score: ",word_score)
    return word_score

#test= get_word_score('max',7)
#print(test)
#test2=get_word_score('zo*',7)
#print(test2)
#test3=get_word_score('b*y',7)
#print(test3)

#
# Make sure you understand how this function works and what it does!
#
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """

    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line
    return 0
#
# Make sure you understand how this function works and what it does!
# You will need to modify this for Problem #4.
#
def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """

    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels):
        x = random.choice(VOWELS_blank)
        hand[x] = hand.get(x, 0) + 1

    for i in range(num_vowels, n):
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1

    return hand

#
# Problem #2: Update a hand by removing letters
#
def update_hand(hand, word):
    """
    Does NOT assume that hand contains every letter in word at least as
    many times as the letter appears in word. Letters in word that don't
    appear in hand should be ignored. Letters that appear in word more times
    than in hand should never result in a negative count; instead, set the
    count in the returned hand to 0 (or remove the letter from the
    dictionary, depending on how your code is structured).

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)
    returns: dictionary (string -> int)
    """

    #pass  # TO DO... Remove this line when you implement this function
    new_hand = hand.copy()
    for i in word.lower():
       if i in new_hand.keys():
          new_hand[i] -=1
          if new_hand[i]==0:
             new_hand.pop(i)
          else:
             pass
       else:
          pass


    #print(new_hand)


    for n in new_hand.keys():
       for j in range(new_hand[n]):
          print(n, end=' ')
    print()
    return new_hand




#
# Problem #3: Test word validity
#
def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.

    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """

    #pass  # TO DO... Remove this line when you implement this function
    word_list=load_words()
    word=word.lower()
    word_fre=get_frequency_dict(word)
#    print(word_fre)
    in_hand=1
    in_list=1

    for i in word:
       if i in hand.keys() and word_fre.get(i,0)<= hand.get(i,0):
          in_hand *= 1
       else:
          in_hand *= 0
          return False
    if in_hand==1:
       if "*" not in word and  word in word_list:
          return True
       elif "*" in word:
          possible_word=[]
          position=word.index("*")
          for w in word_list:
             if len(w)==len(word) and w[position] in VOWELS and word.replace("*","")==w.replace(w[position],""):
                possible_word.append(w)
          if len(possible_word)>0:
             return True
       else:
          return False

#word_list=load_words()
#hand={'h':1,'e':1,'l':2,'o':1}
#word='hello'
#test=is_valid_word(word, hand, word_list)
#print(test)






#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """
    Returns the length (number of letters) in the current hand.

    hand: dictionary (string-> int)
    returns: integer
    """

    #pass  # TO DO... Remove this line when you implement this function
    length = int(len(hand))
    return length

def play_hand(hand, word_list,n):
  hand_length = calculate_handlen(hand)
  current_score = 0
  while hand_length > 0:
    user_word = input("Please make a word or enter '!!' to end the game: ").lower()
    print()
    if user_word != "!!":
      validity = is_valid_word(user_word,hand,word_list)
      if validity == True:
        score = get_word_score(user_word,n)
        print('"',user_word,'"'," earned",score," points")
        current_score += score
        current_hand = update_hand(hand,user_word)
        hand_length = calculate_handlen(current_hand)
        hand = current_hand
        print("current total score: ",current_score)
      else:
        print("choose another word")
        print(current_score)
        current_hand = update_hand(hand,user_word)
        hand_length = calculate_handlen(current_hand)
        hand = current_hand
    else:
      break
  print("End of this game round")
  print(current_score)
  return current_score





   # """
   # Allows the user to play the given hand, as follows:

   # #call initial_hand = deal_hand(n), input (n)
   # # call word_list = load_words()

   # * The hand is displayed.
   # #call display(initial_hand)

   # * The user may input a word.
   # # input a word

   # * When any word is entered (valid or invalid), it uses up letters
   #   from the hand.
   # # call is_valid_word(initial_hand, word, word_list)

   # * An invalid word is rejected, and a message is displayed asking
   #   the user to choose another word.

   # * After every valid word: the score for that word is displayed,
   #   the remaining letters in the hand are displayed, and the user
   #   is asked to input another word.
   #  # if valid: call scrabble_word()
   #  # if valid: call update_hand()
   #  # if valid: call calculated_handlen (current_hand)--> dynamic
   #  len >0 continue the game

   # * The sum of the word scores is displayed when the hand finishes.
   # # cumulate scores --> for /while loop for rounds of hand

   # * The hand finishes when there are no more unused letters.
   #   The user can also finish playing the hand by inputing two
   #   exclamation points (the string '!!') instead of a word.

   #   hand: dictionary (string -> int)
   #   word_list: list of lowercase strings
   #   returns: the total score for the hand

   # """

    # BEGIN PSEUDOCODE <-- Remove this comment when you implement this function
    # Keep track of the total score

    # As long as there are still letters left in the hand:

        # Display the hand

        # Ask user for input

        # If the input is two exclamation points:

            # End the game (break out of the loop)


        # Otherwise (the input is not two exclamation points):

            # If the word is valid:

                # Tell the user how many points the word earned,
                # and the updated total score

            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)

            # update the user's hand by removing the letters of their inputted word


    # Game is over (user entered '!!' or ran out of letters),
    # so tell user the total score

    # Return the total score as result of function



#
# Problem #6: Playing a game
#

def substitute_hand(hand, letter):
    """
    Allow the user to replace all copies of one letter in the hand (chosen by user)
    with a new letter chosen from the VOWELS and CONSONANTS at random. The new letter
    should be different from user's choice, and should not be any of the letters
    already in the hand.

    If user provide a letter not in the hand, the hand should be the same.

    Has no side effects: does not mutate hand.

    For example:
        substitute_hand({'h':1, 'e':1, 'l':2, 'o':1}, 'l')
    might return:
        {'h':1, 'e':1, 'o':1, 'x':2} -> if the new letter is 'x'
    The new letter should not be 'h', 'e', 'l', or 'o' since those letters were
    already in the hand.

    hand: dictionary (string -> int)
    letter: string
    returns: dictionary (string -> int)
    """

   # pass  # TO DO... Remove this line when you implement this function
    choice_letter = VOWELS_blank + CONSONANTS
    substitute =random.choice(choice_letter)
    if hand[letter] > 1:
      hand[letter] -= 1
    else:
      hand.pop(letter)
    hand[substitute]=hand.get(substitute,0)+1
    return hand


#
# procedure you will use to substitute a letter in a hand
#


def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the
      entire series

    * For each hand, before playing, ask the user if they want to substitute
      one letter for another. If the user inputs 'yes', prompt them for their
      desired letter. This can only be done once during the game. Once the
      substitue option is used, the user should not be asked if they want to
      substitute letters in the future.

    * For each hand, ask the user if they would like to replay the hand.
      If the user inputs 'yes', they will replay the hand and keep
      the better of the two scores for that hand.  This can only be done once
      during the game. Once the replay option is used, the user should not
      be asked if they want to replay future hands. Replaying the hand does
      not count as one of the total number of hands the user initially
      wanted to play.

            * Note: if you replay a hand, you do not get the option to substitute
                    a letter - you must play whatever hand you just had.

    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
#    print("play_game not implemented.") # TO DO... Remove this line when you implement this function
    try:
      rounds = int(input("Enter total number of hands: "))
    except ValueError:
      print("Didn't specify the number of hands you want to play. Will just play 1 round. Enjoy!")
      rounds = 1
    n = 1
    total_score = 0
    while n <= rounds:
      try:
        hand_size = int(input("how many letters would you like in a hand? "))
      except ValueError:
        print("Didn't specify hand size. Will play default hand size of 7.")
        hand_size = 7
      print()
      initial_hand = deal_hand(hand_size)
      print("Current hand: ")
      display_hand(initial_hand)

    #try except usage in the middle of the code if I have a few of these sets
      try:
        substitute = input("Do you want to substitute a letter? please enter the lette you want to replace or 'no' to proceed: ").lower()
        if substitute == "no":
          hand_playing = initial_hand
        else:
          hand_playing = substitute_hand(initial_hand,substitute)
      except KeyError:
        print("Didn't specify your choice. Will play the original hand")
        hand_playing = initial_hand

      print("Current hand: ")
      display_hand(hand_playing)

      game_score = play_hand(hand_playing,word_list,hand_size)
      total_score += game_score
      print("Total Score for this hand: ",game_score," points")
      print("------------------------------------")
      n += 1

      if n > rounds:
        break
      else:
        replay = input("Do you want to replay the hand? y/n ")
        if replay == "y":
          print("replay current hand: ")
          display_hand(hand_playing)
          game_score = play_hand(hand_playing, word_list, hand_size)
          total_score += game_score
          print("Total Score for this hand: ",game_score," points")
          print("------------------------------------")
          n += 1

    print("Total score over all hands: ",total_score)

    return 0
#    print("play_game not implemented.") # TO DO... Remove this line when you implement this function

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)

