"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
Kyle Yasumiishi
"""

import poc_fifteen_gui
import random

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        # Returns False if target cell is NOT the zero tile.
        if self.get_number(target_row, target_col) != 0:
            return False
        
        # Returns False if cells to the right of target_col 
        # are NOT positioned in their solved locations.
        if target_col < self.get_width():
            for col in range(target_col + 1, self.get_width()):
                if self.get_number(target_row, col) != col + (target_row * self.get_width()):
                    return False

        # Returns False if cells in rows target_row + 1 and below 
        # are NOT positioned at their solved locations.
        if target_row < self.get_height():
                for row in range(target_row + 1, self.get_height()):
                    for col in range(self.get_width()):
                        if self.get_number(row, col) != col + (row * self.get_width()):
                            return False

        return True

    def position_tile(self, zero_row, zero_col, correct_tile):
        """
        Helper function that returns a string of letters representing
        moves to reposition the tuple, correct_tile (row, col), to 
        the target position (zero_row, zero_col), and 
        the zero tile to the left of the 
        target position (zero_row, zero_col - 1). 
        """
        
        ans = "" 
        vert_dist = abs(zero_row - correct_tile[0])
        horiz_dist = abs(zero_col - correct_tile[1])
        
        # Updates ans, the move string, based the correct_tile's
        # position relative to the target position.
    
        # SAME ROW
        if vert_dist == 0:
            # Left of target
            if zero_col > correct_tile[1]:
                # Moves zero tile left to correct_tile's position.
                ans += str("l" * horiz_dist)
                # Moves correct_tile right to target position,
                # and moves zero tile to left of target position.
                if horiz_dist > 1:
                    ans += str("urrdl" * (horiz_dist - 1))
            # Right of target
            else:
                # Moves zero tile right to correct_tile's position.
                ans += str("r" * horiz_dist)
                # Moves correct_tile left to target position,
                # and moves zero tile to left of target position.
                ans += str("ulldr" * (horiz_dist - 1))
                ans += str("ulld")
  
        # SAME COL
        elif horiz_dist == 0:
            # Moves zero tile up to correct_tile's position.
            ans += str("u" * vert_dist)
            # Moves correct_tile down to target position, 
            # and moves zero tile to left of target position.
            if vert_dist > 1:
                ans += str("lddru" * (vert_dist - 1))
            ans += str("ld")
        
        # UPPER LEFT
        elif correct_tile[1] < zero_col:
            # Moves zero tile up and left to correct_tile's position.
            ans += str("u" * vert_dist)
            ans += str("l" * horiz_dist)
            # Moves correct_tile right and down to target position,
            # and moves zero tile to left of target position.
            ans += str("drrul" * (horiz_dist - 1))
            ans += str("druld" * vert_dist)

        # UPPER RIGHT
        else:
            # Moves zero tile up and right to correct_tile's position.
            ans += str("u" * vert_dist)
            ans += str("r" * horiz_dist)
            # This if-elif-else statement moves correct_tile left and down to target position.
            # If statement is only used when target position is in row 2.
            if vert_dist == 1 and correct_tile[0] == 0:
                ans += str("dllur" * (horiz_dist - 1))
                ans += str("dluld")
            # Elif statement used when correct_tile is in the row above target position.
            elif vert_dist == 1: 
                ans += str("ulldr" * (horiz_dist - 1))
                ans += str("ullddruld")
            # Else statement used when correct_tile is 1+ rows above target position.
            else:
                ans += str("dllur" * (horiz_dist - 1))
                ans += str("dlu")
                ans += str("lddru" * (vert_dist - 1))
                ans += str("ld")
                
        return ans        
               
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        
        assert target_row > 1, "target_row cannot be in rows 0 or 1."
        assert self.lower_row_invariant(target_row, target_col), "tiles to right and below incorrectly ordered"
      
        correct_tile = self.current_position(target_row, target_col)        
        move_str = self.position_tile(target_row, target_col, correct_tile)        
        self.update_puzzle(move_str)
        
        assert self.lower_row_invariant(target_row, target_col - 1), "tiles to right and below incorrectly ordered"
    
        return move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        
        assert target_row > 1, "target_row cannot be in rows 0 or 1."
        assert self.lower_row_invariant(target_row, 0), "tiles to right and below incorrectly ordered"

        # Move zero tile from target position (target_row, 0) to (target_row - 1, 1).
        self.update_puzzle("ur")

        move_str = ""
        
        # correct_tile's position is determined after moving zero tile "ur" 
        # because its position relative to zero tile may have changed as a result.
        correct_tile = self.current_position(target_row, 0)
        
        # Moves to reposition correct_tile to target position.
        if self.get_number(correct_tile[0], correct_tile[1]) != self.get_number(target_row, 0):
            move_str += str(self.position_tile(target_row - 1, 1, correct_tile))
            move_str += str("ruldrdlurdluurddlur")

        # Moves to reposition zero tile to end of column of target_row + 1.
        move_str += str("r" * (self.get_width() - 2))    
        
        self.update_puzzle(move_str)

        assert self.lower_row_invariant(target_row - 1, self.get_width() - 1) 
        
        move_str = "ur" + move_str
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        # Returns False if zero tile is NOT in target position (0, target_col).
        if self.get_number(0, target_col) != 0:
            return False
        
        # Returns False if tiles to the right of target_col are NOT positioned correctly.
        if target_col < self.get_width():
            for col in range(target_col + 1, self.get_width()):
                if self.get_number(0, col) != col:
                    return False
                
        # Returns False if tiles to the right of target_col in row 1 are NOT positioned correctly.
        for col in range(target_col, self.get_width()):
            if self.get_number(1, col) != col + self.get_width():
                return False

        # Returns False if tiles in rows 2 and below are NOT positioned correctly.
        if 1 < self.get_height():
                for row in range(2, self.get_height()):
                    for col in range(self.get_width()):
                        if self.get_number(row, col) != col + (row * self.get_width()):
                            return False

        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        # Returns False if zero tile is NOT in target position (1, target_col).
        if self.get_number(1, target_col) != 0:
            return False
        
        # Returns False if tiles to the right of target_col are NOT positioned correctly.
        if target_col < self.get_width():
            for col in range(target_col + 1, self.get_width()):
                if self.get_number(1, col) != col + (1 * self.get_width()):
                    return False

        # Returns False if tiles in rows 2 and below are NOT positioned correctly.
        if 1 < self.get_height():
                for row in range(2, self.get_height()):
                    for col in range(self.get_width()):
                        if self.get_number(row, col) != col + (row * self.get_width()):
                            return False

        return True

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert target_col > 1, "target_col must be > 1"
        assert self.row0_invariant(target_col), "tiles to right and below incorrectly ordered"
        
        # Move zero tile from target position (0, target_col) to (1, target_col - 1) 
        self.update_puzzle("ld")
        
        move_str = ""

        # correct_tile's position is determined after moving zero tile "ld"
        # because its position relative to zero tile may have changed as a result.
        correct_tile = self.current_position(0, target_col)      
        
        # Moves to reposition correct_tile to target position, and
        # the zero tile to (1, target_col - 1).
        if self.get_number(correct_tile[0], correct_tile[1]) != self.get_number(0, target_col):
            move_str += str(self.position_tile(1, target_col - 1, correct_tile))
            move_str += str("urdlurrdluldrruld")

        self.update_puzzle(move_str)

        assert self.row1_invariant(target_col - 1), "tiles to right and below incorrectly ordered"
        
        move_str = "ld" + move_str
        return move_str

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert target_col > 1, "target_col must be > 1"
        assert self.row1_invariant(target_col), "tiles to right and below incorrectly ordered"

        # Moves correct_tile to the target position (1, target_col),
        # and the zero tile above the target position at (0, target_col). 
        correct_tile = self.current_position(1, target_col)
        move_str = self.position_tile(1, target_col, correct_tile)    
        move_str += "ur"
        self.update_puzzle(move_str)

        assert self.row0_invariant(target_col)
        
        return move_str

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        
        assert self.get_number(1,1) == 0, "zero tile should be at row 1, col 1"
        assert self.row1_invariant(1), "tiles to right and below incorrectly ordered"
        
        # Moves the zero tile to (0,0).
        self.update_puzzle("lu")

        # Repositions the upper left 2x2 part up to 3 times, 
        # each time checking whether the puzzle is solved.
        rotation_num = 0
        if self.row0_invariant(0) == False:
            for dummy_rotation in range(3):
                while self.row0_invariant(0) == False:
                    rotation_num += 1
                    self.update_puzzle("rdlu")

        assert self.row0_invariant(0), "tiles to right and below incorrectly ordered"
        
        move_str = "lu" + ("rdlu" * rotation_num) 
        return move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """

        move_str = ""
           
        # Move zero tile to bottom right corner tile of puzzle.
        zero_pos = self.current_position(0,0)                    
        vert_dist = (self.get_height() - 1) - zero_pos[0]
        horiz_dist = (self.get_width() - 1) - zero_pos[1]
        move_str += (("d" * vert_dist) + ("r" * horiz_dist))
        self.update_puzzle(move_str)
        
        # Solve lower rows
        if self.get_height() > 2:
            for row in range(self.get_height() - 1, 1, -1):
                for col in range(self.get_width() - 1, -1, -1):
                    if col != 0:
                        move_str += self.solve_interior_tile(row, col)
                    else:
                        move_str += self.solve_col0_tile(row)
        
        # Solve top 2 rows
        if self.get_width() > 2:
            for col in range(self.get_width() - 1, 1, -1):
                move_str += self.solve_row1_tile(col)
                move_str += self.solve_row0_tile(col)
        
        # Solve 2x2
        move_str += self.solve_2x2()

        return move_str

#######################################################################################    

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))
    

    
    
    
    
#######################################################################################    
    
import poc_simpletest    

def test():

    suite = poc_simpletest.TestSuite()
    
    #####################################
    
    # TEST lower_row_invariant

    # Tile zero should be positioned at (target_row, target_col)
    puzz = Puzzle(4, 4, initial_grid=[[5,1,2,3],[4,5,6,7],[8,0,10,11],[12,13,14,15]])
    suite.run_test(puzz.lower_row_invariant(2, 2), False, "lower_row_invariant Test 2a:")

    puzz = Puzzle(2,2, initial_grid=[[2,3],[4,0]])
    suite.run_test(puzz.lower_row_invariant(0,0), False, "lower_row_invariant Test 2b:")
    suite.run_test(puzz.lower_row_invariant(0,1), False, "lower_row_invariant Test 2c:")

    # All tiles in rows target_row + 1 or below should be positioned at their solved location
    puzz = Puzzle(4, 4, initial_grid=[[5,1,2,3],[4,5,6,7],[8,0,10,11],[12,4,14,15]])
    suite.run_test(puzz.lower_row_invariant(2, 1), False, "lower_row_invariant Test 3a:")

    puzz = Puzzle(4, 4, initial_grid=[[5,1,2,3],[4,5,6,7],[8,0,10,11],[13,12,14,15]])
    suite.run_test(puzz.lower_row_invariant(2, 1), False, "lower_row_invariant Test 3b:")

    puzz = Puzzle(4, 2, initial_grid=[[5,6],[7,8],[1,2],[3,0]])
    suite.run_test(puzz.lower_row_invariant(3,1), True, "lower_row_invariant Test 3c:")

    puzz = Puzzle(4, 2, initial_grid=[[5,6],[7,8],[1,2],[0,3]])
    suite.run_test(puzz.lower_row_invariant(3,1), False, "lower_row_invariant Test 3d:")

    # Other test cases that should return True
    puzz = Puzzle(4, 4, initial_grid=[[5,1,2,3],[4,5,6,7],[8,0,10,11],[12,13,14,15]])
    suite.run_test(puzz.lower_row_invariant(2, 1), True, "lower_row_invariant Test 4a:")

    ############################################
    
    # TEST solve_interior_tile
    # To test, confirm 1) correct tile ends up in target position, and 
    # 2) zero tile ends up in column to left of target position.
    
    # Tests invariant to make sure can't use method when 
    # target position in either rows 0 or 1.
    # Should just return an AssertionError. If this happens, the test is complete. Comment out test code. 
#    puzz = Puzzle(2, 2, initial_grid=[[2,3],[4,0]])
#    puzz.solve_interior_tile(1,1)
    
    # Correct tile directly above (same col as) target position
    puzz = Puzzle(4, 4, initial_grid=[[4,13,1,3],[5,10,2,7],[8,12,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 1a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 1b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,13,2,7],[8,12,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 2a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 2b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,12,2,7],[8,13,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 3a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 3b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,11],[5,6,7,8],[9,10,4,0]])
    puzz.solve_interior_tile(2,3)
    suite.run_test(puzz.get_number(2,3), 11, "solve_interior_tile Test 4a:")
    suite.run_test(puzz.get_number(2,2), 0, "solve_interior_tile Test 4b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,8],[5,6,7,11],[9,10,4,0]])
    puzz.solve_interior_tile(2,3)
    suite.run_test(puzz.get_number(2,3), 11, "solve_interior_tile Test 5a:")
    suite.run_test(puzz.get_number(2,2), 0, "solve_interior_tile Test 5b:")
                     
    # Correct tile above and to the left of target position
    puzz = Puzzle(4, 4, initial_grid=[[13,4,1,3],[5,10,2,7],[8,12,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 6a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 6b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[13,5,2,7],[8,12,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 7a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 7b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,12,2,7],[13,8,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 8a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 8b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,11,3],[5,6,7,8],[9,10,4,0]])
    puzz.solve_interior_tile(2,3)
    suite.run_test(puzz.get_number(2,3), 11, "solve_interior_tile Test 9a:")
    suite.run_test(puzz.get_number(2,2), 0, "solve_interior_tile Test 9b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,8],[5,6,11,7],[9,10,4,0]])
    puzz.solve_interior_tile(2,3)
    suite.run_test(puzz.get_number(2,3), 11, "solve_interior_tile Test 10a:")
    suite.run_test(puzz.get_number(2,2), 0, "solve_interior_tile Test 10b:")
                                  
    # Correct tile above and to the right of target position              
    puzz = Puzzle(4, 4, initial_grid=[[4,1,3,13],[5,10,2,7],[8,12,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 11a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 11b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,2,13,7],[8,12,6,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 12a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 12b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,12,2,7],[8,6,13,11],[9,0,14,15]])
    puzz.solve_interior_tile(3,1)
    suite.run_test(puzz.get_number(3,1), 13, "solve_interior_tile Test 13a:")
    suite.run_test(puzz.get_number(3,0), 0, "solve_interior_tile Test 13b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,10],[5,6,7,8],[9,4,0,11]])
    puzz.solve_interior_tile(2,2)
    suite.run_test(puzz.get_number(2,2), 10, "solve_interior_tile Test 14a:")
    suite.run_test(puzz.get_number(2,1), 0, "solve_interior_tile Test 14b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,4],[5,6,7,10],[8,9,0,11]])
    puzz.solve_interior_tile(2,2)
    suite.run_test(puzz.get_number(2,2), 10, "solve_interior_tile Test 15a:")
    suite.run_test(puzz.get_number(2,1), 0, "solve_interior_tile Test 15b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,4],[5,6,7,9],[8,0,10,11]])
    puzz.solve_interior_tile(2,1)
    suite.run_test(puzz.get_number(2,1), 9, "solve_interior_tile Test 15a:")
    suite.run_test(puzz.get_number(2,0), 0, "solve_interior_tile Test 15b:")
    
    # Correct tile in same row as target position
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,12,2,7],[8,6,13,11],[9,14,0,15]])
    puzz.solve_interior_tile(3,2)
    suite.run_test(puzz.get_number(3,2), 14, "solve_interior_tile Test 16a:")
    suite.run_test(puzz.get_number(3,1), 0, "solve_interior_tile Test 16b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,12,2,7],[8,6,13,11],[9,15,14,0]])
    puzz.solve_interior_tile(3,3)
    suite.run_test(puzz.get_number(3,3), 15, "solve_interior_tile Test 17a:")
    suite.run_test(puzz.get_number(3,2), 0, "solve_interior_tile Test 17b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,10,1,3],[5,12,2,7],[8,6,13,11],[15,9,14,0]])
    puzz.solve_interior_tile(3,3)
    suite.run_test(puzz.get_number(3,3), 15, "solve_interior_tile Test 18a:")
    suite.run_test(puzz.get_number(3,2), 0, "solve_interior_tile Test 18b:")

    ############################################################
    
    # TEST solve_col0_tile
    
    # Test when correct tile is in target_row - 1
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 1a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 1b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[5,6,7,8],[12,10,11,9],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 2a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 2b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[5,6,7,8],[9,12,11,10],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 3a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 3b:")
    
    # Test when correct tile is above zero tile
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[12,6,7,8],[5,10,11,9],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 4a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 4b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[12,2,3,4],[5,6,7,8],[1,10,11,9],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 5a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 5b:")
    
    # Test when correct tile is not above zero tile
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[5,6,12,8],[9,10,11,7],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 6a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 6b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,12],[5,6,7,8],[9,10,11,4],[0,13,14,15]])
    puzz.solve_col0_tile(3)
    suite.run_test(puzz.get_number(3,0), 12, "solve_col0_tile Test 7a:")
    suite.run_test(puzz.get_number(2, puzz.get_width() - 1), 0, "solve_col0_tile Test 7b:")
    
    # Test when target_row is row 2 (assert invariant won't work at end of this function)
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,4],[5,6,7,8],[0,9,10,11]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(2,0), 8, "solve_col0_tile Test 8a:")
    suite.run_test(puzz.get_number(1, puzz.get_width() - 1), 0, "solve_col0_tile Test 8b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,4],[8,6,7,5],[0,9,10,11]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(2,0), 8, "solve_col0_tile Test 9a:")
    suite.run_test(puzz.get_number(1, puzz.get_width() - 1), 0, "solve_col0_tile Test 9b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,3,8],[5,6,7,4],[0,9,10,11]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(2,0), 8, "solve_col0_tile Test 10a:")
    suite.run_test(puzz.get_number(1, puzz.get_width() - 1), 0, "solve_col0_tile Test 10b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[1,2,8,4],[5,6,7,3],[0,9,10,11]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(2,0), 8, "solve_col0_tile Test 11a:")
    suite.run_test(puzz.get_number(1, puzz.get_width() - 1), 0, "solve_col0_tile Test 11b:")
    
    puzz = Puzzle(3, 4, initial_grid=[[8,2,3,4],[5,6,7,1],[0,9,10,11]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(2,0), 8, "solve_col0_tile Test 12a:")
    suite.run_test(puzz.get_number(1, puzz.get_width() - 1), 0, "solve_col0_tile Test 12b:")
    
    # TEST row1_invariant(j)
    
    puzz = Puzzle(4, 4, initial_grid=[[4,6,1,3],[5,2,0,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(2), True, "row1_invariant Test 1:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,6,1,3],[5,2,7,0],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(3), True, "row1_invariant Test 2:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,6,1,3],[5,2,0,7],[8,9,11,10],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(2), False, "row1_invariant Test 3:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,6,1,3],[5,2,0,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(3), False, "row1_invariant Test 4:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,6,0,3],[5,2,1,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(2), False, "row1_invariant Test 5:")    
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[0,5,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(0), True, "row1_invariant Test 6:")
    
    puzz = Puzzle(4, 4, initial_grid=[[1,2,3,4],[5,0,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row1_invariant(1), True, "row1_invariant Test 6:")
    
    # TEST row0_invariant(j)
    
    puzz = Puzzle(4, 4, initial_grid=[[4,2,0,3],[5,1,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(2), True, "row0_invariant Test 1:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,0,2,3],[5,5,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(1), True, "row0_invariant Test 2:")
    
    puzz = Puzzle(4, 4, initial_grid=[[3,2,0,4],[5,1,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(2), False, "row0_invariant Test 3:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,2,0,3],[5,1,6,7],[8,9,11,10],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(2), False, "row0_invariant Test 4:")
    
    puzz = Puzzle(4, 4, initial_grid=[[0,1,2,3],[4,5,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(0), True, "row0_invariant Test 5:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,2,3,0],[5,1,6,7],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(3), True, "row0_invariant Test 6:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,2,3,0],[5,1,7,6],[8,9,10,11],[12,13,14,15]])
    suite.run_test(puzz.row0_invariant(2), False, "row0_invariant Test 7:")
    
    # TEST solve_row1_tile
    
    puzz = Puzzle(4, 4, initial_grid=[[6,1,2,3],[4,5,0,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row1_tile(2)
    suite.run_test(puzz.get_number(1,2), 6, "solve_row1_tile Test 1a:")
    suite.run_test(puzz.get_number(0,2), 0, "solve_row1_tile Test 1b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[2,1,6,3],[4,5,0,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row1_tile(2)
    suite.run_test(puzz.get_number(1,2), 6, "solve_row1_tile Test 2a:")
    suite.run_test(puzz.get_number(0,2), 0, "solve_row1_tile Test 2b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[5,1,2,3],[4,6,0,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row1_tile(2)
    suite.run_test(puzz.get_number(1,2), 6, "solve_row1_tile Test 3a:")
    suite.run_test(puzz.get_number(0,2), 0, "solve_row1_tile Test 3b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[6,1,2,3],[4,7,5,0],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row1_tile(3)
    suite.run_test(puzz.get_number(1,3), 7, "solve_row1_tile Test 5a:")
    suite.run_test(puzz.get_number(0,3), 0, "solve_row1_tile Test 5b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[6,1,2,7],[4,5,3,0],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row1_tile(3)
    suite.run_test(puzz.get_number(1,3), 7, "solve_row1_tile Test 6a:")
    suite.run_test(puzz.get_number(0,3), 0, "solve_row1_tile Test 6b:")
    
    # TEST solve_row0_tile
    
    puzz = Puzzle(4, 4, initial_grid=[[4,6,1,0],[5,2,3,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row0_tile(3)
    suite.run_test(puzz.get_number(0,3), 3, "solve_row0_tile Test 1a:")
    suite.run_test(puzz.get_number(1,2), 0, "solve_row0_tile Test 1b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,2,1,0],[5,3,6,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row0_tile(3)
    suite.run_test(puzz.get_number(0,3), 3, "solve_row0_tile Test 2a:")
    suite.run_test(puzz.get_number(1,2), 0, "solve_row0_tile Test 2b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,1,0,3],[5,2,6,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row0_tile(2)
    suite.run_test(puzz.get_number(0,2), 2, "solve_row0_tile Test 3a:")
    suite.run_test(puzz.get_number(1,1), 0, "solve_row0_tile Test 3b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[3,6,1,0],[5,2,4,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row0_tile(3)
    suite.run_test(puzz.get_number(0,3), 3, "solve_row0_tile Test 4a:")
    suite.run_test(puzz.get_number(1,2), 0, "solve_row0_tile Test 4b:")
    
    puzz = Puzzle(4, 4, initial_grid=[[5,6,1,0],[3,2,4,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_row0_tile(3)
    suite.run_test(puzz.get_number(0,3), 3, "solve_row0_tile Test 4a:")
    suite.run_test(puzz.get_number(1,2), 0, "solve_row0_tile Test 4b:")

    # TEST solve_2x2
    
    puzz = Puzzle(4, 4, initial_grid=[[5,4,2,3],[1,0,6,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_2x2()
    suite.run_test(puzz.lower_row_invariant(0,0), True, "solve_2x2 Test 1:")
    
    puzz = Puzzle(4, 4, initial_grid=[[1,5,2,3],[4,0,6,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_2x2()
    suite.run_test(puzz.lower_row_invariant(0,0), True, "solve_2x2 Test 1:")
    
    puzz = Puzzle(4, 4, initial_grid=[[4,1,2,3],[5,0,6,7],[8,9,10,11],[12,13,14,15]])
    puzz.solve_2x2()
    suite.run_test(puzz.lower_row_invariant(0,0), True, "solve_2x2 Test 1:")
    
    # OwlTest Tests    
        
    puzz = Puzzle(3, 3, initial_grid=[[8,7,6],[5,4,3],[2,1,0]])
    puzz.solve_interior_tile(2,2)
    suite.run_test(puzz.get_number(2,2), 8, "OwlTest solve_interior_tile Test 1:")
    suite.run_test(puzz.get_number(2,1), 0, "OwlTest solve_interior_tile Test 2:")
    
    # TEST solve_puzzle
    
    puzz = Puzzle(4, 4, initial_grid=[[5,6,4,2],[7,8,10,3],[12,14,1,11],[13,9,15,0]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 1:")
    
    puzz = Puzzle(4, 4, initial_grid=[[6,0,4,2],[5,13,8,3],[12,7,15,14],[9,11,10,1]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 2:")
    
    puzz = Puzzle(4, 4, initial_grid=[[5,4,8,2],[13,6,1,3],[12,11,7,15],[0,9,10,14]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 3:")
    
    puzz = Puzzle(3, 3, initial_grid=[[3,2,8],[6,0,1],[5,4,7]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 4:")
    
    puzz = Puzzle(3, 3, initial_grid=[[8,4,1],[2,5,6],[3,7,0]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 5:")
        
    puzz = Puzzle(2, 2, initial_grid=[[1,3],[0,2]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 6:")
    
    puzz = Puzzle(5, 5, initial_grid=[[1,6,3,9,4],[5,12,0,2,14],
                                      [10,7,11,13,8],[17,16,18,23,19],[15,20,21,22,24]])
    puzz.solve_puzzle()
    suite.run_test(puzz.row0_invariant(0), True, "solve_puzzle Test 1:")    
    
    puzz = Puzzle(4, 4, initial_grid=[[5,6,4,2],[1,7,8,3],[0,9,10,11],[12,13,14,15]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(2,0), 8, "Final Test 1:")
    
    puzz = Puzzle(4, 4, initial_grid=[[5,6,4,2],[1,7,8,3],[0,9,10,11],[12,13,14,15]])
    puzz.solve_col0_tile(2)
    suite.run_test(puzz.get_number(1,3), 0, "Final Test 2:")
    
    suite.report_results()

#test()



##############################################################    

def random_moves(length):
    """
    Generates a list of random moves of a given length for the Fifteen puzzle.
    """
    ans = ""
    for dummy_num in range(length):
        ans += random.choice(["u","d","l","r"])
    return ans    
   
print random_moves(100)


