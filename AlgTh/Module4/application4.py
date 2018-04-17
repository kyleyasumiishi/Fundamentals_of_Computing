"""
Application 4

Use the dynamic programming algorithms implemented in Project 4 to examine
an interesting problem from genomics and analyze words with spelling mistakes.

By: Kyle Yasumiishi
Last Updated: 3/16/2018
"""

############################################################################

# Imports

from module4_provided import *
import project4
import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import math

############################################################################

# CONSTANTS

HUMAN = read_protein(HUMAN_EYELESS_URL)
FLY = read_protein(FRUITFLY_EYELESS_URL)
SCORING_MATRIX = read_scoring_matrix(PAM50_URL)
PAX = read_protein(CONSENSUS_PAX_URL)

############################################################################

# Helper Functions

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    """
    Returns a dictionary scoring_distribution that represents an 
    un-normalized distribution based on the given number of trials num_trials.
    """
    scoring_distribution = {}
    for dummy in range(num_trials):
        y_list = list(seq_y)
        random.shuffle(y_list)
        rand_y = ''.join(y_list)
        alignment_matrix = project4.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        score = project4.compute_local_alignment(seq_x, rand_y, scoring_matrix, alignment_matrix)[0]
        if score in scoring_distribution.keys():
            scoring_distribution[score] = scoring_distribution[score] + 1
        else:
            scoring_distribution[score] = 1
    return scoring_distribution

def get_mean(unnormalized_distribution, num_trials):
    """
    Takes an unnormalized distribution unnormalized_distribution (a dictionary)
    of local alignment scores and number of trials num_trials and returns the mean score.
    """
    total_scores = 0
    for score_key in unnormalized_distribution.keys():
        total_scores += (score_key * unnormalized_distribution[score_key])
    mean = float(total_scores) / num_trials
    return mean

def get_sd(unnormalized_distribution, mean, num_trials):
    """
    Takes an unnormalized distribution unnormalized_distribution (a dictionary)
    of local alignment scores, the mean score, and the number of trials. 
    Returns the standard deviation.
    """
    variance = 0
    for score in unnormalized_distribution.keys():
        num_scores = unnormalized_distribution[score]
        variance += num_scores * (score - mean) ** 2
    variance = float(variance) / num_trials
    standard_deviation = math.sqrt(variance)
    return standard_deviation    

def get_z(local_score, mean, standard_deviation):
    """
    Takes a local alignment score, mean, and standard deviation
    and returns the z-score.
    """
    return (float(local_score) - mean) / standard_deviation

############################################################################

# Application Questions

def question1():
    """
    Compute the local alignments of the sequences of HumanEyelessProtein and
    FruitflyEyelessProtein using the PAM50 scoring matrix.
    """
    # Compute local alignments.
    alignment_matrix = project4.compute_alignment_matrix(HUMAN, FLY, SCORING_MATRIX, global_flag=False)
    local_alignment = project4.compute_local_alignment(HUMAN, FLY, SCORING_MATRIX, alignment_matrix)
    align_human = local_alignment[1]
    align_fly = local_alignment[2]
    print "Human local alignment:", align_human
    print "Fruit fly local alignment:", align_fly
    print "score:", local_alignment[0]
    return (local_alignment[0], align_human, align_fly)
    
def question2():
    """
    Compute the global alignments of local human vs concensus PAX domain
    as well as local fruitfly vs. consensus PAX domain. Return as percentages.
    """
    # Delete any dashes present in local alignments of humans and fruitflies.
    q1 = question1()
    dashless_local_human = q1[1].replace('-','')
    dashless_local_fly = q1[2].replace('-','')
    # Compute global alignments.
    human_alignment_matrix = project4.compute_alignment_matrix(dashless_local_human,PAX,SCORING_MATRIX,False)
    fly_alignment_matrix = project4.compute_alignment_matrix(dashless_local_fly,PAX,SCORING_MATRIX,False)
    human_global = project4.compute_global_alignment(dashless_local_human, PAX, SCORING_MATRIX, human_alignment_matrix)
    fly_global = project4.compute_global_alignment(dashless_local_fly, PAX, SCORING_MATRIX, fly_alignment_matrix)
    # Compute percentage of elements in human_global and fly_global that agree with pax
    human_percent = 0.0
    fly_percent = 0.0
    for char in range(len(human_global[1])):
        if human_global[1][char] == human_global[2][char]:
            human_percent += 1
    for char in range(len(fly_global[1])):
        if fly_global[1][char] == fly_global[2][char]:
            fly_percent += 1
    human_percent = human_percent / len(human_global[1])
    fly_percent = fly_percent / len(fly_global[1])
    print "human_percent:", human_percent
    print "fly_percent:", fly_percent

def question4():
    """
    Using generate_null_distribution, create a distribution of 1000 trials using
    the protein sequences HumanEyelessProtein and FruitflyEyelessProtein with the
    PAM50 scoring matrix. Then, create a bar plot of the normalized version of this
    distribution.
    """
    # Un-normalized distribution created from generate_null_distributions.
    unnormalized = {39: 2, 40: 6, 41: 15, 42: 18, 43: 30, 44: 41, 45: 51, 46: 58, 47: 70, 48: 65, 49: 62, 50: 72, 51: 58, 52: 62, 53: 36, 54: 50, 55: 38, 56: 54, 57: 32, 58: 29, 59: 14, 60: 23, 61: 21, 62: 22, 63: 16, 64: 8, 65: 7, 66: 4, 67: 7, 68: 5, 69: 4, 70: 3, 71: 5, 72: 2, 73: 1, 74: 4, 75: 2, 79: 1, 91: 1, 100: 1}
    # Plot noramlized distribution.
    x_vals = sorted(unnormalized.keys())
    y_vals = [(float(unnormalized[x_val]) / 1000) for x_val in x_vals]
    assert len(x_vals) == len(y_vals), "x-axis and y-axis must have same number of elements"
    plt.bar(x_vals, y_vals)
    plt.gca().set_yticklabels(['{:.0f}%'.format(y*100) for y in plt.gca().get_yticks()])
    plt.xlabel("Local Alignment Scores")
    plt.ylabel("Percent of Number of Trials")
    plt.title("Fraction of 1000 Trials Corresponding to Local Alignment Scores")
    plt.show()

def question5():
    """
    Calculate the mean and standard deviation for the distribution in Question 4, as well as the z-score for the local alignment for the human eyeless protein vs. the fruitfly eyeless protein based on these values.
    """
    unnormalized = {39: 2, 40: 6, 41: 15, 42: 18, 43: 30, 44: 41, 45: 51, 46: 58, 47: 70, 48: 65, 49: 62, 50: 72, 51: 58, 52: 62, 53: 36, 54: 50, 55: 38, 56: 54, 57: 32, 58: 29, 59: 14, 60: 23, 61: 21, 62: 22, 63: 16, 64: 8, 65: 7, 66: 4, 67: 7, 68: 5, 69: 4, 70: 3, 71: 5, 72: 2, 73: 1, 74: 4, 75: 2, 79: 1, 91: 1, 100: 1} 
    mean = get_mean(unnormalized, 1000)
    standard_deviation = get_sd(unnormalized, mean, 1000)
    z_score = get_z(875, mean, standard_deviation)
    print "mean:", mean
    print "standard deviation:", standard_deviation
    print "z-score:", z_score

def question8():
    """
    Implement a simple spelling correction function that uses edit distance to 
    determine whether a given string is the misspelling of a word.
    """    
    # Load list of words
    word_list = read_words(WORD_LIST_URL)

    def check_spelling(checked_word, dist, word_list):
        """
        Iterates through word_list and returns the set of all
        words that are within edit distance dist of the string
        checked_word.
        """
        ans = set([])
        scoring_matrix = project4.build_scoring_matrix('abcdefghijklmnopqrstuvwxyz', 2, 1, 0)
        checked_word_length = len(checked_word)
        for word in word_list:
            word_length = len(word)
            alignment_matrix = project4.compute_alignment_matrix(checked_word, word, scoring_matrix, True)
            global_score = project4.compute_global_alignment(checked_word, word, scoring_matrix, alignment_matrix)
            edit_dist = checked_word_length + word_length - global_score[0]
            if edit_dist <= dist:
                ans.add(word)
        return ans
    
    humble = check_spelling("humble", 1, word_list)
    firefly = check_spelling("firefly", 2, word_list)

    print "humble:", humble
    print "firefly:", firefly

############################################################################

# question1()
# question2()
# question4()
# question5()
question8()




# print generate_null_distribution(HUMAN, FLY, SCORING_MATRIX, 1000)