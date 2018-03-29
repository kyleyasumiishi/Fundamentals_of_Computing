"""Clone of the classic arcade game Pong."""

import simplegui
import random

###############################################################################
# Global variables

WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2

###############################################################################

def new_game():
    """
    Initialize global variables for ball, paddles, and scores.
    """
    global ball_pos, ball_vel
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, ball_pos, ball_vel  
    global score1, score2
    # Initial ball position and velocity
    ball_pos = [(WIDTH / 2), (HEIGHT / 2)]
    ball_vel = [0,0]
    # Initial paddle positions and velocity
    paddle1_pos = HEIGHT / 2
    paddle2_pos = HEIGHT / 2
    paddle1_vel = 0
    paddle2_vel = 0
    # Initial scores
    score1 = 0
    score2 = 0

def spawn_ball(direction):
    """
    Randomly sets the velocity of the ball in the given direction.
    """
    global ball_vel 
    if direction == "right":
        ball_vel[0] = random.randrange(120, 240) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60
    elif direction == "left":
        ball_vel[0] = - random.randrange(120, 240) / 60
        ball_vel[1] = - random.randrange(60, 180) / 60

# Event handlers

def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # draw scores
    canvas.draw_text(str(score1), (WIDTH / 4, HEIGHT * .25), 30, 'blue')
    canvas.draw_text(str(score2), (WIDTH * .75, HEIGHT * .25), 30, 'green')
    
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, 'blue', 'green')
    
    # update ball, keep ball on the screen
    if ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    elif ball_pos[1] >= HEIGHT - BALL_RADIUS:
        ball_vel[1] = - ball_vel[1]
    ball_pos[0] += ball_vel[0] 
    ball_pos[1] += ball_vel[1]
    
    # draw paddles
    canvas.draw_line((HALF_PAD_WIDTH + .5, paddle1_pos + HALF_PAD_HEIGHT), (HALF_PAD_WIDTH + .5, paddle1_pos - HALF_PAD_HEIGHT), PAD_WIDTH, 'red')
    canvas.draw_line((WIDTH - HALF_PAD_WIDTH - .5, paddle2_pos + HALF_PAD_HEIGHT), (WIDTH - HALF_PAD_WIDTH - .5, paddle2_pos - HALF_PAD_HEIGHT), PAD_WIDTH, 'red')
   
    # update paddle's vertical position, keep paddle on the screen
    if paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT and paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_pos += paddle1_vel      
    if paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT and paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_pos += paddle2_vel
    
    # determine whether paddle and ball collide    
    if (ball_pos[0] <= BALL_RADIUS + PAD_WIDTH and 
    (paddle1_pos - HALF_PAD_HEIGHT) < ball_pos[1] < (paddle1_pos + HALF_PAD_HEIGHT)):
        ball_vel[0] = - ball_vel[0] * 1.25
    elif (ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH and 
    (paddle2_pos - HALF_PAD_HEIGHT) < ball_pos[1] < (paddle2_pos + HALF_PAD_HEIGHT)):
        ball_vel[0] = - ball_vel[0] * 1.25
    elif ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        ball_pos = [(WIDTH / 2), (HEIGHT / 2)]
        spawn_ball("right")
        score2 += 1
    elif ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH:
        ball_pos = [(WIDTH / 2), (HEIGHT / 2)]
        spawn_ball("left")
        score1 += 1
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel = -5
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel = 5
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel = -5
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel = 5
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w'] or key == simplegui.KEY_MAP['s']:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP['up'] or key == simplegui.KEY_MAP['down']:
        paddle2_vel = 0

def start():
    """
    Start the game by giving the ball a random direction.
    """
    if random.randint(1, 10) <= 5:
        direction = "left"
    else:
        direction = "right"
    spawn_ball(direction)   

def reset():
    global score1, score2
    new_game()
    score1 = 0
    score2 = 0

###############################################################################
# Create frame

frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Start", start)
frame.add_button("Reset", reset)

# Start frame
new_game()
frame.start()




