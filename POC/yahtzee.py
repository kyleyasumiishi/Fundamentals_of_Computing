"""
Planner for Yahtzee
Simplifications: only allow discard and roll, only score against upper level

Purpose: Learn about combinatorics by writing gen_all_holds
"""

# Used to increase the timeout, if necessary
import codeskulptor, random
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of 
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.
    
    hand: full yahtzee hand
    
    Returns an integer score
    """
    
    max_score = 0
    for die in hand:
        die_score = hand.count(die) * die
        if die_score > max_score:
            max_score = die_score
    return max_score


def convert_set_to_list(a_set):
    """
    Converts the set type to the list type, and returns the list
    If the set contains tuples, then each element of every tuple is added to the list
    """   
    
    original_list = list(a_set)
    converted_list = []
    
    if len(original_list) > 0 and isinstance(original_list[0], tuple):
        for idx in range(len(original_list)):
            for die in original_list[idx]:
                converted_list.append(die)
    else:
        converted_list = original_list

    return converted_list


def expected_value(held_dice, num_die_sides, num_free_dice):
    """ 
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.
    
    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled
    
    Returns a floating point expected value
    """
    
    outcomes = set(range(1, num_die_sides + 1))
    all_rolls = gen_all_sequences(outcomes, num_free_dice)
    roll_probability = 1.0 / len(all_rolls)
    exp_value = 0.0
    
    for roll in all_rolls:
        held_dice_list = convert_set_to_list(held_dice)
        rolled_dice_list = convert_set_to_list(roll)
        
        total_hand_list = []
        total_hand_list.extend(held_dice_list)
        total_hand_list.extend(rolled_dice_list)
        
        roll_expected_value = roll_probability * score(total_hand_list)
        exp_value += roll_expected_value
    
    return exp_value

def gen_all_holds(hand):
    """ 
    Generate all possible choices of dice from hand to hold.
    
    hand: full yahtzee hand
    
    Returns a set of tuples, where each tuple is dice to hold
    """
    
    hand_list = convert_set_to_list(hand)
    num_dice_in_hand = len(hand_list)
    answer_set = set()
    
    # Each tuple in dice_idx_set represents a possible hand, with each element 
    # representing a die's index position in hand_list. 
    dice_idx_set = set([()])

    
    # Note: Each "hand" is simply a collection of dice positions.
    # 1) Generates all possible hands to hold, and stores each hand as a separate tuple in all_unsorted_hands.
    # 2) Sorts the dice positions in each hand, and stores each sorted hand as a separate tuple in all_sorted_hands.
    # 3) Updates dice_idx_set to include set of all_sorted_hands, which, as a set, doesn't include duplicate hands.
    for dummy_idx in range(num_dice_in_hand):
        all_unsorted_hands = set()
        for hand_as_dice_positions in dice_idx_set:
            for die_position in range(num_dice_in_hand):                
                hand_as_dice_positions_list = list(hand_as_dice_positions)
                
                # Prevents a hand from including the same die multiple times
                # by checking whether that die's position is already in the hand.
                if die_position not in hand_as_dice_positions_list:
                    hand_as_dice_positions_list.append(die_position)
                
                all_unsorted_hands.add(tuple(hand_as_dice_positions_list))
 
        all_sorted_hands = [tuple(sorted(hand_as_dice_positions)) for hand_as_dice_positions in all_unsorted_hands]      
        dice_idx_set.update(set(all_sorted_hands))
    
    
    # Converts each hand from dice_idx_set to a hand with actual dice values.
    for hand_as_dice_positions in dice_idx_set:
        hand_as_dice_positions_list = list(hand_as_dice_positions)
        converted_hand_list = []
        for die in range(len(hand_as_dice_positions)):
            converted_hand_list.append(hand_list[hand_as_dice_positions[die]])
        answer_set.add(tuple(converted_hand_list))
       
    return answer_set

def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.
    
    hand: full yahtzee hand
    num_die_sides: number of sides on each die
    
    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    all_holds = gen_all_holds(hand)
    expval_list, all_holds_list, best_dice_to_hold_list = [], [], []
    
    # 1) Calculates expected value for each possible held hand.
    # 2) Stores each possible held hand as tuple in all_holds_list. 
    # 3) Stores expected value corresponding to each held hand in expval_list.
    # Note: The lengths of all_holds_list and expval_list are same.
    for held_dice in all_holds:
        num_free_dice = len(hand) - len(convert_set_to_list(held_dice))
        expval = expected_value(held_dice, num_die_sides, num_free_dice)
        expval_list.append(expval)
        all_holds_list.append(held_dice)
    
    # Maximum expected value from expval_list
    max_expval = max(expval_list) 
    
    # Stores all held hands that result in the max expected value in best_dice_to_hold_list.
    for idx in range(len(all_holds_list)):
        if expval_list[idx] == max_expval:
            best_dice_to_hold_list.append(all_holds_list[idx])
    
    # Randomly chooses hand from best_dice_to_hold_list if there are multiple best hands.
    if len(best_dice_to_hold_list) > 1:
        dice_to_hold = random.choice(best_dice_to_hold_list)
    else:
        dice_to_hold = best_dice_to_hold_list[0]
    
    return (max_expval, dice_to_hold)

def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (1, 1, 1, 5, 6)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand, "is to hold", hold, "with expected score", hand_score


#run_example()

#
#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)



#import poc_simpletest
#
#def run_test():
#    """
#    Some informal testing code
#    """
#    
#    # create a TestSuite object
#    suite = poc_simpletest.TestSuite()
#    
#    outcomes = set([1, 2, 3, 4, 5, 6])
#    
#    # test score 
#    suite.run_test(score([2, 2, 2]), 6, "Test 1:")
#    suite.run_test(score([2, 2, 1]), 4, "Test 2:")
#    suite.run_test(score([2, 1, 5]), 5, "Test 3:")
#    suite.run_test(score([2, 2, 5]), 5, "Test 4:")
#    suite.run_test(score([3, 4, 2, 6, 3]), 6, "Test 5:")
#    suite.run_test(score([2, 4, 4, 4, 6]), 12, "Test 6:")
#
#    # test expected_value
#    suite.run_test(expected_value(set([(2, )]), 6, 1), 4.0, "Test 7:")
#    suite.run_test(expected_value(set([(3, )]), 6, 1), 4.5, "Test 8:")
#    suite.run_test(round(expected_value(set([(2, 2)]), 6, 1), 2), 4.83, "Test 9:")
#    suite.run_test(round(expected_value(set([(4)]), 6, 2), 2), 6.39, "Test 10:")
#    suite.run_test(round(expected_value(set([(3, 3)]), 6, 2), 2), 7.33, "Test 11:")
#    suite.run_test(round(expected_value(set([(4, 3)]), 6, 1), 1), 5.5, "Test 12:")
#    suite.run_test(round(expected_value(set([(6, 6)]), 6, 1), 1), 13.0, "Test 13:")
#    suite.run_test(round(expected_value(set([()]), 6, 1), 1), 3.5, "Test 14:")
#    suite.run_test(round(expected_value(set([(5, )]), 6, 1), 1), 6.0, "Test 15:")
#
#    # test gen_all_holds
#    suite.run_test(gen_all_holds(set([(1, 2)])), set([(), (1, ), (2, ), (1, 2)]), "gen_all_holds Test 1:")
#    
#    # test my understanding of gen_all_sequences
#    suite.run_test(len(gen_all_sequences(outcomes, 2)), 36, "gen_all_sequences Test 1:")
#    suite.run_test(len(gen_all_sequences(outcomes, 3)), 216, "gen_all_sequences Test 2:")
#    
#    # test convert_set_to_list
#    suite.run_test(convert_set_to_list(set([(1, 2, 3, 4, 5, 6)])), [1, 2, 3, 4, 5, 6], "convert_set_to_list Test 1:")
#    suite.run_test(convert_set_to_list(set([(),(1, 2)])), [1, 2], "convert_set_to_list Test 2:")
#    suite.run_test(convert_set_to_list(set([()])), [], "convert_set_to_list Test 3:")
#    suite.run_test(convert_set_to_list(set()), [], "convert_set_to_list Test 4:")
#    suite.run_test(convert_set_to_list(set([1, 2, 3])), [1, 2, 3], "convert_set_to_list Test 5:")
#    
#    # test strategy - make sure to update num dice in function based on each assumption below.
##    suite.run_test(strategy(set([(6, 6)]), 6), (13.0, (6, 6)), "strategy Test 1:")    #assume 3 dice total
##    suite.run_test(strategy(set([(5, )]), 6), (6.0, (5, )), "strategy Test 2:")    #assume 2 dice total
#    
#    suite.report_results()
#    
#run_test()




























