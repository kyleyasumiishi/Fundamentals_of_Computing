"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
#        return self._cells, self._zombie_list, self._human_list # used for testing purposes. can comment out this return
       
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield human
        
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        # Create a new grid, visited, of the same size as
        # the original grid and initialize its cells to be empty.
        visited = [[EMPTY for col in range(self._grid_width)]
                   for row in range(self._grid_height)]
        
        
        # Create a 2D list, distance_field, of the same size as
        # the original grid and initialize each of its entries to be
        # the product of GRID_HEIGHT and GRID_WIDTH (this value
        # is larger than any possible distance).
        distance_field = [[self._grid_height * self._grid_width for col in range(self._grid_width)]
                          for row in range(self._grid_height)]
        
        
        # Create a queue, boundary, that is a copy of either the
        # zombie list or the human list. For cells in the queue, initialize
        # visited to be FULL and distance_field to be zero.
        boundary = poc_queue.Queue()
        
        if entity_type == ZOMBIE:
            for zombie in self.zombies():
                boundary.enqueue(zombie)
                
        elif entity_type == HUMAN:
            for human in self.humans():
                boundary.enqueue(human)
        
        for cell in boundary:
            row = cell[0]
            col = cell[1]
            visited[row][col] = FULL
            distance_field[row][col] = 0            
        
        # Implement a breadth-first search (BFS). For each neighbor_cell
        # in the inner loop, check whether the cell has not been visited and 
        # is passable. If so, update the visited grid and the boundary queue
        # as specified. In this case, also update the neighbor's distance
        # to be the distance to current_cell plus one.
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in neighbors:
                row = neighbor_cell[0]
                col = neighbor_cell[1]
                
                # First checks whether a human/zombie or obstacle is in the neighbor_cell.
                # If neighbor_cell is empty, then sets neighbor_cell to FULL in visited, 
                # adds neighbor_cell to boundary queue, and adds distance to distance_field.
                if (visited[row][col] is EMPTY and self._cells[row][col] is EMPTY): # experiment with is not
                    visited[row][col] = FULL
                    boundary.enqueue(neighbor_cell)
                    distance_field[row][col] = distance_field[current_cell[0]][current_cell[1]] + 1
                      
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
   
        for human_num in range(len(self._human_list)):
            
            greatest_distance = 0
            greatest_distance_list = []
            
            # Creates list of moves, including 8 surrounding cells and current cell
            moves_list = self.eight_neighbors(self._human_list[human_num][0],
                                                      self._human_list[human_num][1])
            moves_list.append(self._human_list[human_num])
            
            # Adds cells without obstacles from moves_list to possible_moves_list
            possible_moves_list = []
            for cell in moves_list:
                if self._cells[cell[0]][cell[1]] is not FULL:
                    possible_moves_list.append(cell)       
            
            # Iterates through each cell in possible_moves_list to determine which
            # cell has the greatest distance in the zombie_distance_field.
            for cell in possible_moves_list:
                if zombie_distance_field[cell[0]][cell[1]] > greatest_distance:
                    greatest_distance = zombie_distance_field[cell[0]][cell[1]]
            
            # Iterates through each cell in possible_moves_list again to determine which
            # cells have the greatest distance and adds these cells to greatest_distance_list.
            for cell in possible_moves_list:
                if zombie_distance_field[cell[0]][cell[1]] == greatest_distance:
                    greatest_distance_list.append(cell)
            
            # Update the human's position to that of the cell with the greatest distance from
            # the nearest zombie. If there are multiple cells with this distance, randomly chooses one.
            best_move = random.choice(greatest_distance_list)
            self._human_list[human_num] = best_move
                    
                
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        
        for zombie_num in range(len(self._zombie_list)):
        
            shortest_distance = self.get_grid_height() * self.get_grid_width()
            shortest_distance_list = []
        
            # Creates list of moves, including 4 neighboring cells and current cells
            moves_list = self.four_neighbors(self._zombie_list[zombie_num][0],
                                             self._zombie_list[zombie_num][1])
            moves_list.append(self._zombie_list[zombie_num])
            
            # Adds cells without obstacles from moves_list to possible_moves_list
            possible_moves_list = []
            for cell in moves_list:
                if self._cells[cell[0]][cell[1]] is not FULL:
                    possible_moves_list.append(cell)
                    
            # Iterates through each cell in possible_moves_list to determine which
            # cell has the shortest distance in the human_distance_field
            for cell in possible_moves_list:
                if human_distance_field[cell[0]][cell[1]] < shortest_distance:
                    shortest_distance = human_distance_field[cell[0]][cell[1]]
                    
            # Iterates through each cell in possible_moves_list again to determine which
            # cells have the shortest distance and adds these cells to shortest_distance_list.
            for cell in possible_moves_list:
                if human_distance_field[cell[0]][cell[1]] == shortest_distance:
                    shortest_distance_list.append(cell)
                    
                    
            # Update the zombie's position to that of the cell with the shortest distance from
            # the nearest zombie. If there are multiple cells with this distance, randomly chooses one.
            best_move = random.choice(shortest_distance_list)
            self._zombie_list[zombie_num] = best_move
            
            # If zombie moves to cell occupied by human(s), adds new zombie(s) to zombie list
            # and remove human(s) from human list
            num_humans_eaten = 0
            
            for human in self.humans():
                if human == best_move:
                    num_humans_eaten += 1
            
            for dummy_num in range(num_humans_eaten):
                self._human_list.remove(best_move)
                self._zombie_list.append(best_move)
            

    
# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
#
######################################################################################

import poc_simpletest

suite = poc_simpletest.TestSuite()

# test clear

apoc_clear = Apocalypse(3, 3, obstacle_list=[(2,2)], zombie_list=[(0,0)], human_list=[(1,1)])

#print apoc_clear

#suite.run_test(apoc_clear.clear(), ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], [], []), "clear test 1:")

# test add_zombie

apoc_add_zombie = Apocalypse(3, 3)
apoc_add_zombie.add_zombie(0,0)
suite.run_test(apoc_add_zombie._zombie_list, [(0,0)], "add_zombie test 1:")
apoc_add_zombie.clear()
suite.run_test(apoc_add_zombie._zombie_list, [], "add_zombie test 2:")

# test num_zombies

apoc_num_zombies = Apocalypse(3, 3, zombie_list=[(0,0), (0,1)])
suite.run_test(apoc_num_zombies.num_zombies(), 2, "num_zombies test 1:")
apoc_num_zombies.add_zombie(2, 2)
suite.run_test(apoc_num_zombies.num_zombies(), 3, "num_zombies test 2:")
apoc_num_zombies.clear()
suite.run_test(apoc_num_zombies.num_zombies(), 0, "num_zombies test 3:")

# test zombie generator

apoc_zombie_gen = Apocalypse(3, 3, zombie_list=[(0,0), (0,1)])
zombie_gen = apoc_zombie_gen.zombies()
suite.run_test(zombie_gen.next(), (0,0), "zombie test 1:")
suite.run_test(zombie_gen.next(), (0,1), "zombie test 2:")
apoc_zombie_gen.clear()
apoc_zombie_gen.add_zombie(1, 1)
zombie_gen = apoc_zombie_gen.zombies()
suite.run_test(zombie_gen.next(), (1,1), "zombie test 3:")

# test add_human

apoc_add_human = Apocalypse(3, 3)
apoc_add_human.add_human(2,2)
suite.run_test(apoc_add_human._human_list, [(2,2)], "add_human test 1:")
apoc_add_human.clear()
suite.run_test(apoc_add_human._human_list, [], "add_human test 2:")

# test num_humans

apoc_num_humans = Apocalypse(3,3, human_list=[(0,0),(0,1),(0,2)])
suite.run_test(apoc_num_humans.num_humans(), 3, "num_humans test 1:")
apoc_num_humans.clear()
suite.run_test(apoc_num_humans.num_humans(), 0, "num_humans test 2:")
apoc_num_humans.add_human(2,2)
suite.run_test(apoc_num_humans.num_humans(), 1, "num_humans test 3:")

# test human generator

apoc_human_gen = Apocalypse(3, 3)
apoc_human_gen.add_human(1,1)
apoc_human_gen.add_human(2,2)
human_gen = apoc_human_gen.humans()
suite.run_test(human_gen.next(), (1,1), "human test 1:")
suite.run_test(human_gen.next(), (2,2), "human test 2:")
suite.run_test(apoc_human_gen.num_humans(), 2, "human test 3:")

# test compute_distance_field

apoc_distance_field = Apocalypse(2, 2, human_list=[(0,0)])
suite.run_test(apoc_distance_field.compute_distance_field(HUMAN), [[0,1],[1,2]], 
               "compute_distance_field test 1:")
apoc_distance_field.add_human(1,1)
suite.run_test(apoc_distance_field.compute_distance_field(HUMAN), [[0,1],[1,0]], 
               "compute_distance_field test 2:")
apoc_distance_field.add_zombie(1,0)
suite.run_test(apoc_distance_field.compute_distance_field(HUMAN), [[0,1],[1,0]], 
               "compute_distance_field test 3:")
suite.run_test(apoc_distance_field.compute_distance_field(ZOMBIE), [[1,2],[0,1]], 
               "compute_distance_field test 4:")


apoc_distance_field2 = Apocalypse(3, 3, obstacle_list=[(1,1)], human_list=[(0,0)], zombie_list=[(2,2)])
suite.run_test(apoc_distance_field2.compute_distance_field(HUMAN), [[0,1,2],[1,9,3],[2,3,4]], 
               "compute_distance_field test 5:")

# test move_humans

apoc_move_humans = Apocalypse(2, 2, human_list=[(0,0)], zombie_list=[(1,0)])
zombie_distance_field = apoc_move_humans.compute_distance_field(ZOMBIE)
apoc_move_humans.move_humans(zombie_distance_field)
suite.run_test(apoc_move_humans._human_list, [(0,1)], "move_humans test 1:")

# test move_zombies

apoc_move_zombies = Apocalypse(3,3, human_list=[(0,0)], zombie_list=[(2,0)])
human_distance_field = apoc_move_zombies.compute_distance_field(HUMAN)
apoc_move_zombies.move_zombies(human_distance_field)
suite.run_test(apoc_move_zombies._zombie_list, [(1,0)], "move_zombies test 1:")
suite.run_test(apoc_move_zombies._human_list, [(0,0)], "move_zombies test 2:")
apoc_move_zombies.move_zombies(human_distance_field)
suite.run_test(apoc_move_zombies._zombie_list, [(0,0),(0,0)], "move_zombies test 3:")
suite.run_test(apoc_move_zombies._human_list, [], "move_zombies test 4:")

suite.report_results()





