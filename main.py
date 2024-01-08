import requests
import random
import os
import platform
from PyDictionary import PyDictionary


# functions for printing out things in color
def prRed(skk): print("\033[1;31m{}\033[00m".format(skk))


def prYellow(skk): print("\033[93m{}\033[00m".format(skk))


def prGreen(skk): print("\033[1;32m{}\033[00m".format(skk))


platform = platform.system()

if platform == 'Windows':
    command = 'cls'
else:
    command = 'clear'


# prints out the game screen
def printScreen():
    print(hangmen[len(wrongGuesses)])  # prints out the hangman drawing based on the number of wrong guesses
    if guessesLeft <= 3:  # if the player has less than 4 guesses left, they get a hint. The hint is just the
        # definition of the word pulled from the PyDictionary module
        dict = dictionary.meaning(word)
        keys = list(dict.keys())
        hint = "Hint: " + dict[keys[0]][0]
        prGreen(hint)
    print("\n")
    print(' '.join(displayCurrent))  # gets rid of brackets, parenthesis, and commas when printing
    print("\n")
    print("Guesses Left:", guessesLeft)
    print("\n")
    # if there is nothing in the wrongGuesses list then it prints none, otherwise, it prints out all the wrong guesses
    if len(wrongGuesses) > 0:
        print("Incorrect Guesses:",
              ' '.join(wrongGuesses))  # gets rid of brackets, parenthesis, and commas when printing
    elif len(wrongGuesses) == 0:
        print("Incorrect Guesses: None")
    print("\n")


# hangman ascii art
hangmen = ['''
    +---+
        |
        |
        |
        |
        |
  =========''', '''
    +---+
    |   |
        |
        |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
        |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
    |   |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|   |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|\  |
        |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|\  |
   /    |
        |
  =========''', '''
    +---+
    |   |
    O   |
   /|\  |
   / \  |
        |
  =========''']

# game title and you win/you lose
title = """\
  
  
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
  by Sam             |___/     
  
  """

youWon = """

 __     __          __          __         _ 
 \ \   / /          \ \        / /        | |
  \ \_/ /__  _   _   \ \  /\  / /__  _ __ | |
   \   / _ \| | | |   \ \/  \/ / _ \| '_ \| |
    | | (_) | |_| |    \  /\  / (_) | | | |_|
    |_|\___/ \__,_|     \/  \/ \___/|_| |_(_)

"""

gameOver = """  
   _____                         ____                 
  / ____|                       / __ \                
 | |  __  __ _ _ __ ___   ___  | |  | |_   _____ _ __ 
 | | |_ |/ _` | '_ ` _ \ / _ \ | |  | \ \ / / _ \ '__|
 | |__| | (_| | | | | | |  __/ | |__| |\ V /  __/ |   
  \_____|\__,_|_| |_| |_|\___|  \____/  \_/ \___|_|   
  
  """


# returns the index of all instances of the player's guess which .index() and .find() can not do.
def findIndex(word, guess):
    return [i for i, letter in enumerate(word) if letter == guess]


while True:

    # Uses request module to grab the list of 10000 words from the site and turns it into one giant array/list 
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    response = requests.get(word_site)
    words = response.content.decode('utf-8').splitlines()

    # setup for PyDictionary module
    dictionary = PyDictionary(words)

    while True:

        # picks a random word from the list of words
        word = words[random.randint(0, len(words))]
        # if the word chosen doesn't pass all the following checks, it will be rerolled

        # checks to see if PyDicitionary has a definition of the word for the hint
        try:
            dictionary.meaning(word)
            keys = list(dict.keys())
        except:
            pass
        # make sure the word has at least 4 characters. There are a lot of words that have 3
        if len(word) < 4:
            pass
        else:
            break

    # lists out the individual characters of the word so it is easier to use in the game
    wordListd = list(word)

    # makes the "_ _ _ _" that shows how many characters that are in the word that is being guessed
    current = "_" * len(word)
    displayCurrent = list(current)

    # stores the wrong guesses that the player makes
    wrongGuesses = []

    guessesLeft = 7
    # create invalid count so an error message is displayed on the next turn if they do something they aren't
    # supposed to do
    invalidCount = 0

    while guessesLeft != 0 and displayCurrent != wordListd:
        if platform == 'Windows':
            os.system(command)
        else:
            os.system(command)
        prYellow(title)
        if invalidCount == 1:
            prRed("Input invalid: Only accepts letters and letters you have not entered yet")
            invalidCount = 0

        printScreen()

        guess = input("Guess a letter:").lower()
        # checks to see if the player entered a number
        try:
            int(guess)
        except:
            pass

        else:
            invalidCount += 1
            continue
        # checks to see if player entered more than one character
        if len(guess) > 1:
            invalidCount += 1
            continue
        # checks to see if player entered nothing
        elif guess == ' ':
            invalidCount += 1
            continue
        # checks to see if player already made that guess before
        elif guess in wrongGuesses or guess in displayCurrent:
            invalidCount += 1
            continue
        # checks to see if their guess is correct if it gets through all the previous checks
        elif guess in wordListd:
            guessIndex = findIndex(word, guess)
            # replace the corresponding place holder "_" with the correct guess that the person made
            for i in range(len(guessIndex)):
                displayCurrent[guessIndex[i]] = wordListd[guessIndex[i]]
            # if the guess was wrong, take away one of their guesses and add the wrong guess to the list of wrong guesses
        else:
            guessesLeft -= 1
            wrongGuesses.append(guess)
        # enter game over screen if the player loses
    if guessesLeft == 0:
        os.system(command)
        prRed(gameOver)
        print("The word was:", word)
        userContinue = input("Play Again? (Yes/No):").lower
        if userContinue == "yes":
            break
        elif userContinue == "no":
            print("Goodbye!")
            exit()

    # enter you won screen if the player wins
    else:
        os.system(command)
        prGreen(youWon)
        print("The word was:", word)
        userContinue = input("Play Again? (Yes/No):").lower

        if userContinue == "yes":
            break

        elif userContinue == "no":
            print("Goodbye!")
            exit()
