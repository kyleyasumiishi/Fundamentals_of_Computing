# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random

# global variables
SECRET_NUM = random.randrange(0, 100)	
MAX_GUESSES = 7
CURRENT_GUESS = 0

# helper function to start and restart the game
def new_game():
    """
    Resets current guess number CURRENT_GUESS to 0.
    """    
    global CURRENT_GUESS
    CURRENT_GUESS = 0
    
# define event handlers for control panel
def range100():
    """
    Starts a new game, with a range of [0, 100).
    """
    global MAX_GUESSES, SECRET_NUM
    MAX_GUESSES = 7
    SECRET_NUM = random.randrange(0, 100)
    print "Guess a number between 0-99 in " + str(MAX_GUESSES) + " guesses. Good luck!"
    return new_game()
    
def range1000():
    """
    Starts a new game, with a range of [0, 1000).
    """
    global MAX_GUESSES, SECRET_NUM
    MAX_GUESSES = 10
    SECRET_NUM = random.randrange(0, 1000)
    print "Guess a number between 0-999 in " + str(MAX_GUESSES) + " guesses. Good luck!"    
    return new_game()
    
def input_guess(guess):
    """
    Converts the string guess to an integer, and compares it with the secret number SECRET_NUM.
    """
    global CURRENT_GUESS 
    # Converts guess to integer.
    guess_int = int(guess)
    print "Guess was " + str(guess_int)
    # Increments global variable CURRENT_GUESS.
    CURRENT_GUESS += 1
    remaining_guesses = MAX_GUESSES - CURRENT_GUESS
    # Compares guess to SECRET_NUM.
    if (remaining_guesses == 0) and (guess_int != SECRET_NUM):
        print "Game over. Secret number was " + str(SECRET_NUM) + "."
        new_game()
    elif guess_int < SECRET_NUM:
        print "Higher"
        print "Remaining guesses: " + str(remaining_guesses)
    elif guess_int > SECRET_NUM:
        print "Lower"
        print "Remaining guesses: " + str(remaining_guesses)
    else:
        print "Correct. Secret number was " + str(SECRET_NUM) + "."
        new_game()
    
# create frame
frame = simplegui.create_frame("Guess the number", 300, 300)

# register event handlers for control elements and start frame
input = frame.add_input("Enter Guess", input_guess, 100)
newgame100 = frame.add_button("New Game: 100", range100, 100)
newgame1000 = frame.add_button("New Game: 1000", range1000, 100)                        

# call new_game 
new_game()
