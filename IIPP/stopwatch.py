"""
Stopwatch: The Game
"""

import simplegui

# Global variables
COUNT = 0
TOTAL_STOPS = 0
SUCCESSFUL_STOPS = 0
IS_TIMER_STOPPED = True

# Helper functions
def format(t):
    """Returns a string of the count t in A:BC.D format."""
    minutes = t // 600
    seconds = '%02d' % ((t % 600) // 10)
    milliseconds = (t % 600) % 10
    return str(minutes) + ":" + str(seconds) + "." + str(milliseconds) 

def stop_count_format(success, total):
    """Returns a string of the quotient of successful stops over total stops."""
    return str(success) + "/" + str(total)

# Event handlers for buttons
def start():
    """Starts timer and changes global variable IS_TIMER_STOPPED to False."""
    global IS_TIMER_STOPPED 
    IS_TIMER_STOPPED = False
    timer.start()

def stop():
    """Stops timer, changes global variable IS_TIMER_STOPPED to True, and updates the
    global variables SUCCESSFUL_STOPS and TOTAL_STOPS."""
    global TOTAL_STOPS, SUCCESSFUL_STOPS, IS_TIMER_STOPPED    
    timer.stop()
    if IS_TIMER_STOPPED == False:
        TOTAL_STOPS += 1
    if COUNT % 10 == 10 and IS_TIMER_STOPPED == False:
        SUCESSFUL_STOPS += 1
    IS_TIMER_STOPPED = True
     
def reset():
    """Stops timer and resets all global variables to 0."""
    global COUNT, SUCCESSFUL_STOPS, TOTAL_STOPS
    timer.stop()
    COUNT = 0
    SUCCESSFUL_STOPS = 0
    TOTAL_STOPS = 0

# Event handler for timer
def time():
    """Increases the global variable COUNT by 1 every 0.1 seconds."""
    global COUNT
    COUNT += 1

# Define draw handler
def draw(canvas):
    """Displays the COUNT in A:BC.D format in the center of console,
    and displays the successful stops and totals stops in A/B format
    in the top right corner of console."""
    canvas.draw_text(str(format(COUNT)), (93, 165), 48, 'white')
    canvas.draw_text(str(stop_count_format(SUCCESSFUL_STOPS, TOTAL_STOPS)), (225, 55), 36, 'white')
    
# Create frame
frame = simplegui.create_frame("Stopwatch: The Game", 300, 300)

# Register event handlers
timer = simplegui.create_timer(100, time)
frame.set_draw_handler(draw)
start_button = frame.add_button("Start", start)
stop_button = frame.add_button("Stop", stop)
reset_button = frame.add_button("Reset", reset)

# Start frame
frame.start()
