# Problem Set 4B
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    #print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    #print("  ", len(wordlist), "words loaded.")
    return wordlist


def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story_ps4.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words_ps4.txt'

"""superclass Message - not supposed to be called directly"""
class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''
        self.message_text=text
        self.valid_words=load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''
        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''
        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        full_lowercase = string.ascii_lowercase
        full_lowercase_list = list(full_lowercase)
        full_uppercase=string.ascii_uppercase
        full_uppercase_list=list(full_uppercase)

        letter=self.get_message_text()
       # print(letter)
        if letter in full_lowercase:
            letter_position=full_lowercase_list.index(letter)
            #shift up
            mapping_pos = (letter_position+shift)%26

            #shift down
            #mapping_pos=(letter_position-shift)

            mapping=full_lowercase_list[mapping_pos]
        else:
            letter_position=full_uppercase_list.index(letter)
            #shift up
            mapping_pos = (letter_position+shift)%26

            #shift down
            #mapping_pos=(letter_position-shift)

            mapping=full_uppercase_list[mapping_pos]
        mapping_letter=dict()
        mapping_letter[letter]=mapping
       # print(mapping_letter)
        return mapping_letter


    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
             down the alphabet by the input shift
        '''
        message=self.get_message_text()
        #print(message)
        new_string_list = []
        for letter in message:
        #    print(letter)
            letter=Message(letter)
            mapping_dict=letter.build_shift_dict(shift)
            for v in mapping_dict.values():
                new_string_list.append(v)
       # print(new_string_list)
        new_string=''.join(new_string_list)
        return new_string

#test=Message('text')
##test_m=test.get_message_text()
#change=test.apply_shift(2)
#print(change)

'''subclass PlaintextMessage'''
class PlaintextMessage(Message):
    def __init__(self, text,shift=None):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self,text)
        self.shift=shift

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''

        self.shift=shift

        #return 0# self.shift
    def encryption_dict(self):
        shift=self.shift
        for t in text:
            #print(t)
            t=Message(t)
            return t.build_shift_dict(shift) #don't need self seems like

            '''if =self.build_shift_dict(shift), self would still be 'text' which
            wouldn't be in the ascii list - not a letter'''

            '''don't need self.encryption_dict = t.build_shift_dict(shift); plus
            it didn't work with self.change_shift for some reason'''
    def message_text_encrypted(self):
        shift=self.shift
        #print(shift)
        return self.apply_shift(shift)




    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''
        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''
        shift=self.get_shift
        return self.encryption_dict.copy
        '''no need bracket in the end - return self.build_shift_dict.copy()
        without() seems to return function type instead of calling a function'''


    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''
        shift=self.get_shift
        return self.message_text_encrypted()




#test2=PlaintextMessage('text',5)
#n = test2.message_text_encrypted()
#print(n)
#
#change=test2.change_shift(2)
#print(test2.get_shift())
#print(test2.shift)
#print(type(test2))
#nn=test2.message_text_encrypted()
#
#print(nn)
#print(type(test2))
#shift_2=test2.change_shift(2)
#shift = test2.get_shift() #shift updated to 2
#print(shift)
#change = test2.get_message_text_encrypted()
#shift_change=test2.get_shift()
#print(shift_change)
#print(change)
#


class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        Message.__init__(self,text)

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''
        shift = 0
        de_message=self.apply_shift(shift)
        #print(decrypt_message)
        word_list=self.valid_words
        #print(word_list)
        validWord = is_word(word_list,de_message)

        while validWord != True:
            shift += 1
            de_message=self.apply_shift(shift)
            validWord = is_word(word_list,de_message)

            if shift == 26:
                break

        word_pair=[shift,de_message]
        basket=tuple(word_pair)
        return basket
#            words_pair[self]=decrypt_message
#            basket.append(words_pair)
#




if __name__ == '__main__':

    #Example test case (PlaintextMessage)
    #plaintext = PlaintextMessage('hello', 2)
    #print('Expected Output: jgnnq')
    #print('Actual Output:', plaintext.get_message_text_encrypted())
    '''test passed'''

    #Example test case (CiphertextMessage)
    ciphertext = CiphertextMessage('jgnnq')
    print('Expected Output:', (24, 'hello'))
    print('Actual Output:', ciphertext.decrypt_message())

    #TODO: WRITE YOUR TEST CASES HERE

    #TODO: best shift value and unencrypted story

    pass #delete this line and replace with your code here
