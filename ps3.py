# 6.0001 Problem Set 3
#
# The 6.0001 Word Game
# Created by: Kevin Luu <luuk> and Jenna Wiens <jwiens>
#
# Name          : Arshak
# Time spent    : 1:40 + 2:00 + 0:30 + 2:00 + 2:00

import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10,}

# -----------------------------------
# Helper code
# (you don't need to understand this helper code)

WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
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
    s=0
    for i in word.lower():
        s+= SCRABBLE_LETTER_VALUES.get(i,0)#if i in SCRABBLE_LETTER_VALUES.keys(): s+=SCRABBLE_LETTER_VALUES[i]
    return s*max(1, 7*len(word)-3*(n-len(word)))
    
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

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand["*"] = 0
    
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
    hand = hand.copy()
    word = word.lower()    
    for i in word:
        if hand.get(i,0)>0:
            hand[i]-=1
        if hand.get(i,-1)==0:
            del(hand[i])
    return hand
####    hand = hand.copy()
####    for i in word.lower():
####        if i in hand.keys():
####            hand[i] = hand.get(i, 0) - 1
####        if hand[i]==0: del hand[i]
####    return hand
##print(update_hand({'a':1, 'q':1, 'l':2, 'm':1, 'u':1, 'i':1}, 'quail'))
#
# Problem #3: Test word validity
#

def show_possible_matches(my_word, word_list):
    match = ''
    for i in word_list:
        if match_with_gaps(my_word, i):match += i + " "
    if len(match) == 0:
        return False
    match=match.split(' ')
    del match[-1]
    return match

def match_with_gaps(my_word, other_word):
    h = 0
    word = ''.join(my_word.split())
    if len(word) == len(other_word):
      for i, word1 in enumerate(word):
        if word1 == other_word[i] or word1 == '*':
          h += 1
          if h == len(other_word):
            return True
    return False

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

##    if word.lower() not in word_list: return False
##    if len(word.lower())>=len(hand):
##        return all(i in word.lower() for i in hand)
##    return False 
    
    word=word.lower()
    number=0
    if word in word_list:#not in word_list: return False
        for i in word:
            if i in hand.keys():
                if hand[i]<word.count(i):
                    return False
            else: number+=1
        if number > 0: return False
        return True
    else:
        if not show_possible_matches(word, word_list):
            return False
        else:
            for i in show_possible_matches(word, word_list):
                if i[word.index('*')] in VOWELS:
                     return True
                else:
                     return False
    return False


#
# Problem #5: Playing a hand
#
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    return sum(hand.values())

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.
 
      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    totalscore=0
##    display_hand(hand)
    while calculate_handlen(hand)>0:
        print('Current Hand: ', end='')
        display_hand(hand)
        #display_hand(hand)
        #print("Current hand: ") #;print(display_hand(hand))
        word=input('Enter word, or "!!" to indicate that you are finished: ')
        if word == '!!':
            break
        else:
            if is_valid_word(word, hand, word_list):
                totalscore+=get_word_score(word, calculate_handlen(hand))
                print('"'+ word+ '"', "earned:", str(get_word_score(word, calculate_handlen(hand))) + ". Total:", totalscore, 'points')
            else:
                print("That is not a valid word. Please choose another word.")
        print()
##        print('before', hand)
        hand=update_hand(hand, word)
##        print('after', hand)
    if len(hand)<=0: print("Ran out of letters. Total score: ", totalscore, 'points.')
    else: print( "Total score: ", totalscore, "points.")
##play_hand({'a':1, 'j':1, 'e':1, 'f':1, '*':1, 'r':1, 'x':1}, load_words())
####play_hand({'a':1, 'c':1, 'f':1, 'i':1, '*':1, 't':1, 'x':1}, load_words())

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


#
# procedure you will use to substitute a letter in a hand
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
    
    if letter not in hand: return hand
    win=False
    while not win:
        x=random.choice(VOWELS+CONSONANTS)
        if x not in hand:
            d1={x: hand[letter]}
            hand.update(d1)
            del hand[letter]
            return hand
##print(substitute_hand({'a':10, 'd':2, 'r':1, 'g':3}, 'g'))
    
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
        
    numhand=int(input("Enter total number of hands: "))
    hand=deal_hand(7)
    print('Current Hand: ', end='')
    display_hand(hand)
    s = input("Would you like to substitute a letter? ")
    if s == 'yes':
        letter= input("Which letter would you like to replace: ")
        substitute_hand(hand,letter)
    play_hand(hand, word_list)
    
        

#
# Build data structures used for entire session and play game
# Do not remove the "if __name__ == '__main__':" line - this code is executed
# when the program is run directly, instead of through an import statement
#
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
