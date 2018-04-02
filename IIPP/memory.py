"""
Memory card game
"""

import simplegui
import random

# Global variables
card_pos = 0, 50
half_deck1 = [0, 1, 2, 3, 4, 5, 6, 7]
half_deck2 = list(half_deck1)
deck = half_deck1 + half_deck2
exposed = list(deck)
state = 0
Match = []
Exposed1 = 0
Exposed2 = 0
pos1 = 200
pos2 = 200
turns = 0

# Helper function to initialize globals
def new_game():
    global deck, exposed, Exposed1, Exposed2, pos1, pos2, Match, state, turns
    random.shuffle(deck)
    Exposed1 = 0
    Exposed2 = 0
    pos1 = 200
    pos2 = 200
    Match = []
    exposed = list(deck)
    state = 0
    turns = 0
    
# Define event handlers
def mouseclick(pos):
    """
    Event handler for mouse clicks that takes the position of the mouse click pos, flips cards based on the location, and determines if flipped cards match.
    """
    global state, pos1, pos2, Exposed1, Exposed2, turns
    # 1st click of game or turn. Exposes 1st clicked card.
    if state == 0:
        state = 1
        pos1 = int(pos[0])
        exposed[pos1 // 50] = "Exposed"
        Exposed1 = deck[pos1 // 50]
    
    # 2nd click. Keeps 1st clicked card exposed and exposes the 2nd clicked card.
    elif state == 1:
        state = 2
        pos2 = int(pos[0])
        if pos1 // 50 != pos2 // 50:
            turns += 1
            exposed[pos2 // 50] = "Exposed"
            Exposed2 = deck[pos[0] // 50]
        else: state = 1
    
    # 3rd click. If 1st and 2nd card match, keep both exposed. 
    # Otherwise, flip both over. Expose next clicked card.
    else:
        state = 1
        if Exposed1 == Exposed2:
            Match.extend([pos1 // 50, pos2 // 50])
        else:
            exposed[pos1 // 50] = "Not exposed"
            exposed[pos2 // 50] = "Not exposed"
        pos1 = int(pos[0])
        exposed[pos1 // 50] = "Exposed"
        Exposed1 = deck[pos[0] // 50]   
  
def draw(canvas):
    """
    Draw cards to the canvas. Cards are 50x100 pixels in size.
    """
    global card_pos
    label.set_text("Turns = " + str(turns))
    for card_index in range(len(deck)):
        card_pos = 25 + 50 * card_index, 50
        if card_index in Match:
            canvas.draw_text(str(deck[card_index]), card_pos, 10, "White")
        elif exposed[card_index] == "Exposed":
            canvas.draw_text(str(deck[card_index]), card_pos, 10, "White")
        else:
            canvas.draw_polygon([(card_pos[0] - 25, 0), (card_pos[0] - 25, 100), (card_pos[0] + 25, 100), (card_pos[0] + 25, 0)], 1, "Black", "Green")

# Create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")
label.set_text(str(turns))

# Register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# Start game
new_game()
frame.start()