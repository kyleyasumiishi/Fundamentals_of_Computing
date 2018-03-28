"""
Clone of 2048 game.
"""

import poc_2048_gui, random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    temp_list = []
    merged_list = []
    
    # Add non-zeroes from line to temp_list.
    for num in range(len(line)):
        if line[num] != 0:
            temp_list.append(line[num])
        else:
            pass
    
    # Merge non-zeroes from temp_list. 
    # If two tiles merge, prevent double merging by adding a zero to temp_list.
    for num in range(1,len(temp_list)):
        if temp_list[num] == temp_list[num - 1]:
            temp_list[num - 1] *= 2
            temp_list[num] = 0
        else:
            pass
    
    # Add non-zeroes from temp_list to merged_list.
    for num in range(len(temp_list)):
        if temp_list[num] != 0:
            merged_list.append(temp_list[num])
        else:
            pass

    # Add trailing zeroes to merged_list until len(merged_list) == len(line).
    if len(merged_list) < len(line):
        for num in range(len(merged_list),len(line)):
            merged_list.append(0)  
    
    return merged_list

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        
        # create grid
        self._grid = [[0 for col in range(self._width)] for row in range(self._height)]
        
        # reset game 
        self.reset()
        
        # initial tiles for each direction
        self._initial_tiles_up = []
        self._initial_tiles_down = []
        self._initial_tiles_left = []
        self._initial_tiles_right = []
        
        for row in range(self._height):
            self._initial_tiles_left.append((row, 0))
            self._initial_tiles_right.append((row, self._width - 1))
        
        for col in range(self._width):
            self._initial_tiles_up.append((0, col))
            self._initial_tiles_down.append((self._height - 1, col))
            
        self._initial_tiles_dic = {1: self._initial_tiles_up, 2: self._initial_tiles_down,
                                  3: self._initial_tiles_left, 4: self._initial_tiles_right}
        
   
#    def dic_test_up(self):
#        """
#        Used to test whether dictionary is set up properly.
#        """
#        
#        return self._initial_tiles_dic[1]
#    
#    def dic_test_left(self):
#        return self._initial_tiles_dic[3]
#    
#    def dic_test_down(self):
#        return self._initial_tiles_dic[2]
#    
#    def dic_test_right(self):
#        return self._initial_tiles_dic[4]
    
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
               
        for row in range(self._height):
            for col in range(self._width):
                self._grid[row][col] = 0
                
        # comment out calls to new_tile for testing
        self.new_tile()
        self.new_tile()
        
#        return self._grid

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        for row in range(len(self._grid)):
            print self._grid[row]
        print
                
        return str(self._grid)
        
    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self._width

    def move(self, dirval):
        """
        Move all tiles in the given direction (dirval) and add
        a new tile if any tiles moved.
        
        This method works as follows:
        1. Uses the direction in the OFFSETS dictionary to iterate over the 
        entries of the associated row or column (traversal_dir) starting at the specified intial tile (start_row, start_col).
        It retrieves the tile values from those entries, and stores them in temp_list.
        
        2. Calls the  merge function to merge the tile values in temp_list.
        
        3. Iterates over the entries in traversal_dir and stores merged tile values back into grid.
        
        4. If any tiles move, add new tile.
        """
        
        # traversal_dir (transveral direction) is grid height for UP and DOWN, grid width for LEFT and RIGHT.
        # This variable obviates the need for duplicate code for each iteration of the
        # associated row or col (traversal_dir), which depends on direction.
        if dirval == 1 or dirval == 2:
            traversal_dir = self.get_grid_height()
        else:
            traversal_dir = self.get_grid_width()
        
        # By default, assumes move method won't change grid. If it does, this boolean 
        # changes to True and a new tile is added.
        is_grid_changed = False
        
        # First iteration is over each initial tile of the initial tiles list for a particular direction.
        # Each initial tile has a start_row and start_col, which is its location on the grid.
        for tile in range(len(self._initial_tiles_dic[dirval])):
             
            temp_list = []
            start_row = self._initial_tiles_dic[dirval][tile][0]
            start_col = self._initial_tiles_dic[dirval][tile][1]
            
            # Second iteration is over traversal_dir. Each tile's value, starting with initial tile's, is
            # added to temp_list.
            for tile in range(traversal_dir):
                row = start_row + (tile * OFFSETS[dirval][0])
                col = start_col + (tile * OFFSETS[dirval][1])
                temp_list.append(self.get_tile(row, col))
            
            # Merges temp_list
            merged_temp_list = merge(temp_list)
            
            # If any tiles merged, then this boolean changes to True, which will cause a new tile to be added.
            if merged_temp_list != temp_list:
                is_grid_changed = True

            # Final iteration is over traversal_drtn again. The values from merged_temp_list replace each tile's old value.
            for tile in range(traversal_dir):
                row = start_row + (tile * OFFSETS[dirval][0])
                col = start_col + (tile * OFFSETS[dirval][1])
                self.set_tile(row, col, merged_temp_list[tile])
                
        # comment out call to new_tile for testing
        if is_grid_changed:
            self.new_tile()
        
#        return self._grid

    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        empty_square_list = []
        
        # Identify all empty squares in self._grid and appends empty_square_list with
        # list [row, col] representing location.
        for row in range(self.get_grid_height()):
            for col in range(self.get_grid_width()):
                if self._grid[row][col] == 0:
                    empty_square_list.append([row, col])
                else:
                    pass
        
        # Assign a value of 2 or 4.
        random_int = random.randint(1, 10)
        if random_int == 10:
            value = 4
        else:
            value = 2
            
        # Randomly choose a list from empty_square_list and update self._grid at that location.
        if len(empty_square_list) > 0:
            random_square = random.choice(empty_square_list)
            self.set_tile(random_square[0], random_square[1], value)
        else:
            pass   

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value
        
        # comment out return - used for testing purposes
#        return str(self._grid)

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]
    
    
    
    

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
#    # create a TwentyFortyEight object
#    FourbyFour_2048 = TwentyFortyEight(4,4)
#    FivebyFive_2048 = TwentyFortyEight(5,5)
#    FivebyThree_2048 = TwentyFortyEight(5,3)
#    TwobyTwo_2048 = TwentyFortyEight(2,2)
#    
#    TwobyTwo_2048.set_tile(0, 0, 2)
#    TwobyTwo_2048.set_tile(0, 1, 2)
#    TwobyTwo_2048.set_tile(1, 0, 0)
#    TwobyTwo_2048.set_tile(1, 1, 0)
#    
#    ThreebyTwo_2048 = TwentyFortyEight(3,2)
#    
#    ThreebyTwo_2048.set_tile(0, 0, 4)
#    ThreebyTwo_2048.set_tile(0, 1, 0)
#    ThreebyTwo_2048.set_tile(1, 0, 2)
#    ThreebyTwo_2048.set_tile(1, 1, 2)
#    ThreebyTwo_2048.set_tile(2, 0, 2)
#    ThreebyTwo_2048.set_tile(2, 1, 2)
#        
#    # test get_grid_height method
#    suite.run_test(FourbyFour_2048.get_grid_height(), 4, "Test #1:")
#    suite.run_test(FivebyFive_2048.get_grid_height(), 5, "Test #2:")
#    suite.run_test(FivebyThree_2048.get_grid_height(), 5, "Test #3:")
#    
#    # test get_grid_width method
#    suite.run_test(FourbyFour_2048.get_grid_width(), 4, "Test #4:")
#    suite.run_test(FivebyFive_2048.get_grid_width(), 5, "Test #5:")
#    suite.run_test(FivebyThree_2048.get_grid_width(), 3, "Test #6:")
#    
#    # test to see if grid dimensions are correct. Run before new tiles. Should be all zeroes. 
#    suite.run_test(str(FourbyFour_2048._grid), str([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]), "Test #7:")
#    suite.run_test(str(FivebyFive_2048._grid), str([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]), "Test #8:")
#    suite.run_test(str(FivebyThree_2048._grid), str([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]), "Test #8:")
#    
#    # test set_tile method
#    suite.run_test(FourbyFour_2048.set_tile(1, 1, 17), str([[0, 0, 0, 0], [0, 17, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]), "Test #9:")
#    suite.run_test(FivebyFive_2048.set_tile(3, 4, 14), str([[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 14], [0, 0, 0, 0, 0]]), "Test #10:")
#    suite.run_test(FivebyThree_2048.set_tile(4, 2, 5), str([[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 5]]), "Test #11:")
#    
#    # test get_tile method
#    suite.run_test(FourbyFour_2048.get_tile(1, 1), 17, "Test 12:")
#    suite.run_test(FivebyFive_2048.get_tile(3, 4), 14, "Test 13:")
#    suite.run_test(FivebyThree_2048.get_tile(1, 1), 0, "Test 14:")
#    
#    # test dic_test
#    suite.run_test(FourbyFour_2048.dic_test_up(), [(0, 0), (0, 1), (0, 2), (0, 3)], "Test 15:")
#    suite.run_test(FivebyFive_2048.dic_test_left(), [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)], "Test 16:")
#    suite.run_test(FivebyThree_2048.dic_test_right(), [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)], "Test 17:")
#    suite.run_test(FourbyFour_2048.dic_test_down(), [(3, 0), (3, 1), (3, 2), (3, 3)], "Test 18:")
#    
#    # to test the move functions, make sure to test one direction at a time and 
#    # comment out the other directions. Otherwise, it'll move the grid and the other
#    # tests will come up with errors.
#    
#    # test move - UP
##    suite.run_test(TwobyTwo_2048.move(1), [[2, 2], [0, 0]], "Test 19:")
##    suite.run_test(ThreebyTwo_2048.move(1), [[4, 4], [4, 0], [0, 0]], "Test 20:")
#    
#    # test move - DOWN
##    suite.run_test(TwobyTwo_2048.move(2), [[0, 0], [2, 2]], "Test 21:")
##    suite.run_test(ThreebyTwo_2048.move(2), [[0, 0], [4, 0], [4, 4]], "Test 22:")
#    
#    # test move - LEFT
##    suite.run_test(TwobyTwo_2048.move(3), [[4, 0], [0, 0]], "Test 23:")
##    suite.run_test(ThreebyTwo_2048.move(3), [[4, 0], [4, 0], [4, 0]], "Test 24:")
#    
##    # test move - RIGHT
##    suite.run_test(TwobyTwo_2048.move(4), [[0, 4], [0, 0]], "Test 25:")
##    suite.run_test(ThreebyTwo_2048.move(4), [[0, 4], [0, 4], [0, 4]], "Test 26:")
#    
#    suite.report_results()
#    
##run_test()

#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

