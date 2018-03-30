import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10, '*':0}

WORDLIST_FILENAME = "words.txt"

def load_words():
    
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
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	
def get_word_score(word, n):

    s=0
    for i in word.lower():
        s+= SCRABBLE_LETTER_VALUES.get(i,0)
    return s*max(1, 7*len(word)-3*(n-len(word)))
    
def display_hand(hand):
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      
    print()                             
 
def deal_hand(n):

    hand={}
    num_vowels = int(math.ceil(n / 3))

    for i in range(num_vowels - 1):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1

    hand["*"] = 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
    
    return hand

def update_hand(hand, word):

    hand = hand.copy()
    word = word.lower()    
    for i in word:
        if hand.get(i,0)>0:
            hand[i]-=1
        if hand.get(i,-1)==0:
            del(hand[i])
    return hand

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
    
    word=word.lower()
    number=0
    x=0
    t=0
    if word in word_list:
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
            for k in word:
                if k =='*':
                    x+=1
                    if x>1: return False
            for i in show_possible_matches(word, word_list):
                if i[word.index('*')] in VOWELS and '*' in hand:
                    for s in i:
                        if s!='*' and s in hand: t+=1
                        if t==len(word)-1: return True
                else:
                     return False
    return False

def calculate_handlen(hand):

    return sum(hand.values())

def play_hand(hand, word_list):

    totalscore=0
    while calculate_handlen(hand)>0:
        print('Current Hand: ', end='')
        display_hand(hand)
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
        hand=update_hand(hand, word)
    if len(hand)<=0: print("Ran out of letters. Total score: ", totalscore, 'points.')
    else: print( "Total score: ", totalscore, "points.")
    return totalscore

def substitute_hand(hand, letter):
    
    if letter not in hand: return hand
    win=False
    while not win:
        x=random.choice(VOWELS+CONSONANTS)
        if x not in hand:
            d1={x: hand[letter]}
            hand.update(d1)
            del hand[letter]
            return hand
    
def play_game(word_list):
  
    numhand=input("Enter total number of hands: ")
    totalscore=0
    n=1
    for i in range(int(numhand)):
        hand=deal_hand(HAND_SIZE)
        if totalscore==0:
            print('Current Hand: ', end='')
            display_hand(hand)
        if n>0:
            s=''
            while s not in ['yes','no']:
                s=input("Would you like to substitute a letter? ")
                if s.lower()=='yes':
                    n-=1
                    letter= input("Which letter would you like to replace: ")
                    hand=substitute_hand(hand,letter)
            print()
        totalscore+=play_hand(hand, word_list)
        print('----------')
        replay=''
        while replay not in ['yes', 'no']:
            replay=input("Would you like to replay the hand? ")
        if replay=='yes': totalscore+=play_hand(hand, word_list)
    print("Total score over all hands:", totalscore)

if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
