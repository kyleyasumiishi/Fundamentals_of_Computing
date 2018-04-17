"""
Project 4

Implements four functions. The first pair of functions returns matrices
used to compute the alignment of two sequences. The second pair of functions
returns global and local alignments of two input sequences based on a 
provided alignment matrix.

By: Kyle Yasumiishi
Last Updated: 3/15/2018
"""

import math

##############################################################

# Helper functions

def get_score(seq_x, seq_y, scoring_matrix):
    """
    Helper function that returns the score of two sequences of equal length
    seq_x and seq_y from a scoring matrix scoring_matrix.
    """
    assert len(seq_x) == len(seq_y), "Sequences must be same length"
    score = 0
    for idx in range(len(seq_x)):
        score += scoring_matrix[seq_x[idx]][seq_y[idx]]
    return score

def get_max_val_loc(alignment_matrix):
    """
    Helper function that returns the maximum value 
    and the maximum value's row and column in 
    alignment_matrix as a tuple
    (max_val, max_val_row, max_val_col).
    """
    max_val = 0
    max_val_row = 0
    max_val_col = 0
    for row in range(len(alignment_matrix)):
        for col in range(len(alignment_matrix[row])):
            val = alignment_matrix[row][col]
            if val > max_val:
                max_val = val
                max_val_row = row
                max_val_col = col
    return (max_val, max_val_row, max_val_col)

def gen_local_alignment_matrix(alignment_matrix, max_val, max_val_row, max_val_col):
    """
    Helper function that takes an input alignment matrix
    alignment_matrix and returns a new matrix whose last cell
    is the maximum value max_val from alignment_matrix.
    """
    assert alignment_matrix[max_val_row][max_val_col] == max_val, "The maximum value must be at the correct location"
    new_matrix = alignment_matrix[:max_val_row + 1]
    for row in range(len(new_matrix)):
        new_matrix[row] = new_matrix[row][:max_val_col + 1]
    assert new_matrix[-1][-1] == max_val, "max_val must be value of last cell in new_matrix"
    return new_matrix

##############################################################

# Project 4 Questions

def build_scoring_matrix(alphabet, diag_score, off_diag_score, dash_score):
    """
    Taks as input a set of characters alphabet and three scores
    diag_score, off_diag_score, and dash_score. The function returns 
    a dictionary of dictionaries whose entries are indexed by pairs
    of characters in alphabet plus '-'. The score for any entry indexed
    by one or more dashes is dash_score. The score for the remaining
    diagonal entries is diag_score. Finally, the score for the remaining
    off-diagonal entries is off_diag_score.
    """
    # Initialize scoring matrix as dictionary of dictionaries.
    scoring_matrix = {char: {} for char in alphabet}
    scoring_matrix['-'] = {}
    # Score dictionary entries.
    for row_char in scoring_matrix.keys():
        for col_char in scoring_matrix.keys():
            if row_char == '-' or col_char == '-':
                scoring_matrix[row_char][col_char] = dash_score
            elif row_char != col_char:
                scoring_matrix[row_char][col_char] = off_diag_score
            else:
                scoring_matrix[row_char][col_char] = diag_score
    return scoring_matrix

def compute_alignment_matrix(seq_x, seq_y, scoring_matrix, global_flag):
    """
    Takes as input two sequences seq_x and seq_y whose elements share
    a common alphabet with the scoring matrix scoring_matrix. The 
    function computes and returns the alignment matrix for seq_x and seq_y
    as described in the Homework. If global_flag is True, each entry of 
    the alignment matrix is computed using the method described in Question 8
    of the Homework. If global_flag is False, each entry is computed
    using the method described in Question 12 of the Homework. 
    """
    len_x = len(seq_x)
    len_y = len(seq_y)
    # Initialize alignment matrix as list of lists.
    alignment_matrix = [[0 for dummy_y in range(len_y + 1)] for dummy_x in range(len_x + 1)]
    # Row 0 alignment scores
    for x_idx in range(1, len_x + 1):
        alignment_matrix[x_idx][0] = alignment_matrix[x_idx - 1][0] + scoring_matrix[seq_x[x_idx - 1]]['-']
    # Col 0 alignment scores
    for y_idx in range(1, len_y + 1):
        alignment_matrix[0][y_idx] = alignment_matrix[0][y_idx - 1] + scoring_matrix['-'][seq_y[y_idx - 1]]
    # Local pairwwise alignment adjustment for row 0 and col 0.
    if global_flag == False:
        for row in range(len_x + 1):
            if alignment_matrix[row][0] < 0:
                alignment_matrix[row][0] = 0
        for col in range(len_y + 1):
            if alignment_matrix[0][col] < 0:
                alignment_matrix[0][col] = 0
    # Compute alignment scores.
    for x_idx in range(1, len_x + 1):
        for y_idx in range(1, len_y + 1):
            alignment_matrix[x_idx][y_idx] = max(alignment_matrix[x_idx - 1][y_idx - 1] + scoring_matrix[seq_x[x_idx - 1]][seq_y[y_idx - 1]],
                                                 alignment_matrix[x_idx - 1][y_idx] + scoring_matrix[seq_x[x_idx - 1]]['-'],
                                                 alignment_matrix[x_idx][y_idx - 1] + scoring_matrix['-'][seq_y[y_idx - 1]]) 
            # Local pairwise alignment adjustment
            if alignment_matrix[x_idx][y_idx] < 0 and global_flag == False:
                alignment_matrix[x_idx][y_idx] = 0

    return alignment_matrix

def compute_global_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a 
    common alphabet with the scoring matrix scoring_matrix. This function
    computes a global alignment of seq_x and seq_y using the global alignment
    matrix alignment_matrix. The function returns a tuple of the form
    (score, align_x, align_y) whose score is the score of the global alignment
    align_x and align_y. Note that align_x and align_y should have the same length
    and may include the padding character '-'.
    """
    x_idx = len(seq_x)
    y_idx = len(seq_y)
    align_x = ""
    align_y = ""
    while x_idx > 0 and y_idx > 0:
        # Up left
        if alignment_matrix[x_idx][y_idx] == alignment_matrix[x_idx - 1][y_idx - 1] + scoring_matrix[seq_x[x_idx - 1]][seq_y[y_idx - 1]]:
            align_x += seq_x[x_idx - 1]
            align_y += seq_y[y_idx - 1]
            x_idx -= 1
            y_idx -= 1
        # Up
        elif alignment_matrix[x_idx][y_idx] == alignment_matrix[x_idx - 1][y_idx] + scoring_matrix[seq_x[x_idx - 1]]['-']:
            align_x += seq_x[x_idx - 1]
            align_y += '-'
            x_idx -= 1
        # Left
        else:
            align_x += '-'
            align_y += seq_y[y_idx - 1]
            y_idx -= 1
    while x_idx > 0:
        align_x += seq_x[x_idx - 1]
        align_y += '-'
        x_idx -= 1
    while y_idx > 0:
        align_x += '-'
        align_y += seq_y[y_idx - 1]
        y_idx -= 1
    # Reverse global alignment strings.
    align_x = align_x[::-1]
    align_y = align_y[::-1]
    # Feasability invariants.
    assert len(align_x) == len(align_y), "Length of align_x and align_y must be equal"
    for idx in range(len(align_x)):
        if align_x[idx] == '-':
            assert align_y[idx] != '-', "There cannot exist an i such that x_align[i] = y_align[i] = '-'."
    score = get_score(align_x, align_y, scoring_matrix)
    return (score, align_x, align_y)

def compute_local_alignment(seq_x, seq_y, scoring_matrix, alignment_matrix):
    """
    Takes as input two sequences seq_x and seq_y whose elements share a common
    alphabet with the scoring matrix scoring_matrix. This function computes a 
    local alignment of seq_x and seq_y using the local alignment matrix
    alignment_matrix. The function returns a tuple of the form (score, align_x, align_y)
    where score is the score of the optimal local alignment align_x and align_y.
    Note that align_x and align_y should have the same length and may include the
    padding character '-'.
    """
    # Compute new alignment matrix whose last cell contains maximum value from alignment_matrix.
    max_val_loc = get_max_val_loc(alignment_matrix)
    new_matrix = gen_local_alignment_matrix(alignment_matrix, max_val_loc[0], max_val_loc[1], max_val_loc[2])
    # Compute local alignments.
    local_alignment = compute_global_alignment(seq_x[:max_val_loc[1]], seq_y[:max_val_loc[2]], scoring_matrix, new_matrix)
    align_x = local_alignment[1]
    align_y = local_alignment[2]
    # Remove leading characters until score equals maximum value from alignment_matrix.
    start_char = 0
    for char_idx in range(len(align_x)):
        temp_score = get_score(align_x[char_idx:], align_y[char_idx:], scoring_matrix)
        if temp_score < max_val_loc[0]:
            start_char += 1
        else:
            break
    align_x = align_x[start_char:]
    align_y = align_y[start_char:]
    score = get_score(align_x, align_y, scoring_matrix)
    return (score, align_x, align_y)

