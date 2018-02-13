"""
Mini-max Tic-Tac-Toe Player
Kyle Yasumiishi
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}    

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    
    # Base case
    winner = board.check_win()
    
    if winner == provided.PLAYERX:
        return (SCORES[provided.PLAYERX], (-1, -1))
    elif winner == provided.PLAYERO:
        return (SCORES[provided.PLAYERO], (-1, -1))
    elif winner == provided.DRAW:
        return (SCORES[provided.DRAW], (-1, -1))
    
    # Recursive case
    else:
        # For each empty square, creates a clone of board and
        # player moves on that square. Then recursively calls
        # mm_move function with cloned board. Returns the 
        # score that minimizes the maximum loss
        # (-1 for Player O, +1 for Player X).
        
        scores_and_moves = []     # list of tuples of (score, (row, col))
        empty_squares = board.get_empty_squares()
        next_player = provided.switch_player(player)

        for square in empty_squares:
            clone = board.clone()
            clone.move(square[0], square[1], player)
            scores_and_moves.append((mm_move(clone, next_player)[0], square))
            
            # This if-elif statement will return once the first square 
            # that minimizes the maximum loss is found.
            if player == provided.PLAYERX and scores_and_moves[-1][0] == 1:
                return scores_and_moves[-1]
            elif player == provided.PLAYERO and scores_and_moves[-1][0] == -1:
                return scores_and_moves[-1]
                     
        if player == provided.PLAYERX:
            return sorted(scores_and_moves)[-1]
        else: 
            return sorted(scores_and_moves)[0]
                  
def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

#######################################################################################

import poc_simpletest

def run_test():
    """
    Some informal testing code
    """
    
    # Create a TestSuite object
    
    suite = poc_simpletest.TestSuite()
    
    # Test mm_move 
    
    board = provided.TTTBoard(3, board=[[2, 3, 3],[2, 2, 3],[2, 1, 1]])
    suite.run_test(mm_move(board, provided.PLAYERX), (1, (-1, -1)), "Test 1:")
    
    board = provided.TTTBoard(3, board=[[2, 3, 3],[3, 2, 2],[3, 2, 3]])
    suite.run_test(mm_move(board, provided.PLAYERX), (0, (-1, -1)), "Test 2:")
    
    board = provided.TTTBoard(3, board=[[3, 3, 3],[3, 2, 2],[3, 2, 2]])
    suite.run_test(mm_move(board, provided.PLAYERX), (-1, (-1, -1)), "Test 3:")
    
    board = provided.TTTBoard(3, board=[[3, 2, 2],[3, 2, 1],[1, 3, 2]])
    suite.run_test(mm_move(board, provided.PLAYERO), (-1, (2, 0)), "Test 4:")
    
    board = provided.TTTBoard(3, board=[[3, 2, 1],[3, 2, 1],[2, 3, 2]])
    suite.run_test(mm_move(board, provided.PLAYERO), (0, (0, 2)), "Test 5:")
    
    board = provided.TTTBoard(3, board=[[3, 2, 1],[3, 2, 2],[1, 3, 2]])
    suite.run_test(mm_move(board, provided.PLAYERO), (-1, (2, 0)), "Test 6:")
    
    board = provided.TTTBoard(3, board=[[3, 2, 1],[3, 2, 1],[1, 3, 2]])
    suite.run_test(mm_move(board, provided.PLAYERX), (0, (2, 0)), "Test 7:")

    suite.report_results()

#run_test()

########################################################################################


# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)

