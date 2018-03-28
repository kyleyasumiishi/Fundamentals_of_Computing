# Rock-paper-scissors-lizard-Spock template

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:

# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions

import random

def name_to_number(name):
    """
    Helper function that converts the string name into a number between 0 and 4.
    """
    if name == "rock":
        return 0
    elif name == "Spock":
        return 1
    elif name == "paper":
        return 2
    elif name == "lizard":
        return 3
    elif name == "scissors":
        return 4
    else:
        print "Input string 'name' must be either: rock, Spock, paper, lizard, or scissors."

def number_to_name(number):
    """
    Helper function that converts a number in the range 0 to 4 into its corresponding name as a string.
    """
    if number == 0:
        return "rock"
    elif number == 1:
        return "Spock"
    elif number == 2:
        return "paper"
    elif number == 3:
        return "lizard"
    elif number == 4:
        return "scissors"
    else:
        print "Input number 'number' must be either: 0, 1, 2, 3, or 4."

def rpsls(player_choice): 
    """
    Prints the winner of player_choice and a randomly generated computer choice. 
    """
    # print a blank line to separate consecutive games
    print
    # print out the message for the player's choice
    print "Player chooses " + str(player_choice) + "."
    # convert the player's choice to player_number using the function name_to_number()
    player_number = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randint(0, 4)
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    # print out the message for computer's choice
    print "Computer chooses " + str(comp_choice) + "."
    # compute difference of comp_number and player_number modulo five
    difference = (player_number - comp_number) % 5
    # use if/elif/else to determine winner, print winner message
    if difference == 0:
        print "Tie!"
    elif difference == 1 or difference == 2:
        print "Player wins!"
    else:
        print "Computer wins!"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

