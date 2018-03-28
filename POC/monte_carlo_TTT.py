"""
Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player

# Add your functions here.

def mc_trial(board, player):
    """
    This function plays a game starting with the given player
    by making random moves, alternating between players. 
    Function modifies the board input, and returns when the game is over.
    """
    for dummy in range(len(board.get_empty_squares())):
        while board.check_win() == None:
            random_empty_square = random.choice(board.get_empty_squares())
            board.move(random_empty_square[0], random_empty_square[1], player)
            player = provided.switch_player(player)

def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists)
    with the same dimensions as the TTT board, a board from
    a completed game, and which player the machine player is.
    Function scores the completed board and updates the scores grid.
    As the function updates the scores grid directly, it does not return anything.
    """  
    winner = board.check_win()
    dim = board.get_dim()

    for col in range(dim):
        for row in range(dim):
            square = board.square(row, col)
            
            # Iteration occurs only when game does not end in a draw.
            if winner != provided.DRAW:
                
                # If player wins, player's squares increase those squares' scores by SCORE_CURRENT and 
                # opponent's squares decrease those squares' scores by SCORE_OTHER. Empty squares don't affect scores.
                if winner == player:
                    if square == winner:
                        scores[row][col] += SCORE_CURRENT
                    elif square != provided.EMPTY:
                        scores[row][col] -= SCORE_OTHER
                            
                # If player loses, player's squares decrease those squares' scores by SCORE_CURRENT and
                # opponent's squares increase those squares' scores by SCORE_OTHER. Empty squares don't affect scores.
                elif winner != player:
                    if square == winner:
                        scores[row][col] += SCORE_OTHER
                    elif square != provided.EMPTY:
                        scores[row][col] -= SCORE_CURRENT

def get_best_move(board, scores):
    """
    Function finds all of the empty squares with the maximum score
    and randomly return one of them as a (row, column) tuple.
    """
    max_score = -1 * NTRIALS    # max_score not initially 0 because scores can go negative.
    empty_squares = board.get_empty_squares()
    max_score_tuple_list = []
    
    # For loop iterates through empty_squares list to set max_score equal to 
    # the corresponding maximum score in scores list.
    for tup in range(len(empty_squares)):
        row = empty_squares[tup][0]
        col = empty_squares[tup][1]
        if scores[row][col] >= max_score:
            max_score = scores[row][col]
    
    # For loop iterates through empty_squares list after max_score is determined
    # to add tuples(s) that correspond to max_score to max_score_tuple_list.
    for tup in range(len(empty_squares)):
        row = empty_squares[tup][0]
        col = empty_squares[tup][1]
        if scores[row][col] == max_score:
            max_score_tuple_list.append((row, col))
                
    # Returns a random tuple from max_score_tuple_list.
    if len(max_score_tuple_list) >= 1:
        return random.choice(max_score_tuple_list)
    
def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine 
    player is, and the number of trials to run.
    Function uses the Monte Carlo simulation to return a move for
    the machine player in the form of a (row, column) tuple. 
    """
    dim = board.get_dim()
    scores = [[0 for dummycol in range(dim)] for dummyrow in range(dim)]
    
    for dummy_trial in range(trials):
        board_clone = board.clone()
        mc_trial(board_clone, player)
        mc_update_scores(scores, board_clone, player)
    
    # Returns best move returned by get_best_move function
    return get_best_move(board, scores)
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

#provided.play_game(mc_move, NTRIALS, False)        
#poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

