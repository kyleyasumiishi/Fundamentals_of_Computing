"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._total_time = 0.0
        self._cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]

        
    def __str__(self):
        """
        Return human readable state
        """
        
        state_string = str("Total number of cookies produced: " + str(self.get_total_cookies()) + "\n"
                       "Current number of cookies: " + str(self.get_cookies()) + "\n"
                       "Current time: " + str(self.get_time()) + "\n"
                       "Current CPS: " + str(self.get_cps()))
        
        return state_string

    
    def get_total_cookies(self):
        """
        Return total number of cookies
        
        Should return a float
        """
          
        return float(self._total_cookies)    
                
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return float(self._current_cookies)
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return float(self._cps)
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return float(self._total_time)
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        
        return list(self._history)

    
    def get_last_item(self):
        """
        Return last item purchased
        
        Used for testing purposes"""
        
        history_list = self.get_history()
        
        return history_list[-1][1]
    
    def print_history(self):
        """
        Prints state/history of the game for debugging purposes.
        """
        
        history_list = list(self.get_history())
        
        print "Time:", str(self.get_time())
        print "Last item:", str(history_list[-1][1])
#        print "Cost of last item:", str(history_list[-1][2])
        print "Current cookies:", str(self.get_cookies())
        print "Total cookies:", str(self.get_total_cookies())
        print "CPS:", str(self.get_cps())
        
    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """

        if self.get_cookies() >= cookies:
            seconds = 0.0    
        else:    
            seconds = float(math.ceil((cookies - self.get_cookies()) / self.get_cps()))
        
        return seconds
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        
        if time <= 0.0:
            pass
        else:
            additional_cookies = self.get_cps() * time
            self._total_time += time
            self._current_cookies += additional_cookies
            self._total_cookies += additional_cookies

    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        
        if self.get_cookies() < cost:
            pass
        else:
            self._current_cookies -= cost
            self._cps += additional_cps
            self._history.append((self.get_time(), item_name, float(cost), self.get_total_cookies()))
            
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """  

    state = ClickerState()
    clone = build_info.clone()
#    count = 0    # Used solely for debugging. 
    
    while state.get_time() <= duration:        
        
#        count += 1
        time_left = duration - state.get_time()
        
        # Determine next_item to buy via strategy function. Exit loop if None.
        next_item = strategy(state.get_cookies(), state.get_cps(), state.get_history(), time_left, clone)  
        if next_item == None:
            break
   
        # Determine cost of next_item.
        cost_next_item = clone.get_cost(next_item)

        # Determine wait time until you have enough cookies to buy next_item.
        time_until_next_item = state.time_until(cost_next_item)
        
        # If time_until_next_item is within sim duration: wait, buy item, and update clone.
        if time_until_next_item <= time_left:
            state.wait(time_until_next_item)
            state.buy_item(next_item, cost_next_item, clone.get_cps(next_item))
            clone.update_item(next_item)
        else:
            break

    # If applicable, continue accumulating cookies until end of sim duration.         
    if duration - state.get_time() > 0:
        state.wait(duration - state.get_time())
       
#    print "Number of iterations:", count
    state.print_history()

    return state


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"


def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None


def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    # cost_item_list includes tuple of (cost, item) for each buildable item, sorted by lowest cost.
    cost_item_list = sorted([(build_info.get_cost(item), item) for item in build_info.build_items()])
    cheapest_item = None
    max_cookies = cookies + (cps * time_left)
    
    for cost_item_tup in cost_item_list:
        if max_cookies >= cost_item_tup[0]:
            cheapest_item = cost_item_tup[1]
            break
    
    return cheapest_item


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    
    # cost_item_list includes tuple of (cost, item) for each buildable item, sorted by highest cost.
    cost_item_list = sorted([(build_info.get_cost(item), item) for item in build_info.build_items()], reverse=True)
    most_expensive_item = None
    max_cookies = cookies + (cps * time_left)

    for cost_item_tup in cost_item_list:
        if max_cookies >= cost_item_tup[0]:
            most_expensive_item = cost_item_tup[1]
            break
                
    return most_expensive_item
    

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    
    This strategy returns the item with the lowest marginal cost
    (cookie cost per additional CPS) that you can 
    afford in the time left.
    """
    
    # mc_item_list includes tuple of (marginal cost, item) for each buildable item, sorted by lowest mc.
    # mc = cost / cps
    mc_item_list = sorted([((build_info.get_cost(item) / build_info.get_cps(item)), item) for 
                           item in build_info.build_items()])
    best_item = None
    max_cookies = cookies + (cps * time_left)
    
    for mc_item_tup in mc_item_list:
        if max_cookies >= build_info.get_cost(mc_item_tup[1]):
            best_item = mc_item_tup[1]
            break
            
    return best_item
    

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
#run()


#import poc_simpletest 
#
#suite = poc_simpletest.TestSuite()
#
#initial_state = ClickerState()
#
## test initial ClickerState methods
#
#suite.run_test(initial_state.get_cookies(), 0.0, "initial get_cookies:")
#suite.run_test(initial_state.get_cps(), 1.0, "initial get_cps:")
#suite.run_test(initial_state.get_time(), 0.0, "initial get_time:")
#suite.run_test(initial_state.get_history(), [(0.0, None, 0.0, 0.0)], "initial get_history:")
#suite.run_test(initial_state.time_until(10), 10.0, "time_until #1:")
#suite.run_test(initial_state.time_until(10.0), 10.0, "time_until #2:")
#suite.run_test(initial_state.time_until(0), 0.0, "time_until #3:")
#
#initial_state.wait(5)
#
#suite.run_test(initial_state.get_cookies(), 5.0, "get_cookies after 5 sec:")
#suite.run_test(initial_state.get_cps(), 1.0, "get_cps after 5 sec:")
#suite.run_test(initial_state.get_time(), 5.0, "get_time after 5 sesc:")
#
## test ClickerState buy_item and get_history methods
#
#modified_initial_state = ClickerState()
#modified_initial_state._total_cookies = 100
#modified_initial_state._current_cookies = 100
#
#modified_initial_state.buy_item("Item Example", 25, 1.0)
#
#suite.run_test(modified_initial_state.get_history(), [(0.0, None, 0.0, 0.0), (0.0, "Item Example", 25.0, 100.0)], "get_history:")
#
#modified_initial_state.wait(5)
#
#suite.run_test(modified_initial_state.get_cookies(), float(100 - 25 + 10), "get_cookies:")

##################################################

# test simulate_clicker with strategy_cursor_broken

#suite.run_test(simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_cursor_broken).get_last_item(), "Cursor", "strategy_cursor_broken:")

#suite.report_results()




###################################################

#simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_cursor_broken)    
#simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_cheap)
#simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_expensive)
#simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_best)
#simulate_clicker(provided.BuildInfo(), SIM_TIME, strategy_none)
    
    
    
    
    
    

