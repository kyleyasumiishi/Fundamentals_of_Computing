# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
started = False
counter = 0

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated
   
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

def process_sprite_group(canvas, group):
    remove_set = set([])
    for s in group:
        s.update()
        s.draw(canvas)
        if s.age > s.lifespan:			
            remove_set.add(s)			
    group.difference_update(remove_set)
  
def group_collide(group, other_object):
    global explosion_group
    remove_set = set([])
    for sprite in list(group):
        if sprite.collide(other_object):
            explosion_sprite = Sprite(sprite.get_position, [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion_sprite)
            remove_set.add(sprite)
            group.difference_update(remove_set)
            return True

def group_group_collide(group1, group2):
    global score
    remove_set = set([])
    for sprite in list(group1):
        if group_collide(group2, sprite):
            score += 5
            remove_set.add(sprite)
            group1.difference_update(remove_set) 

# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.info = info
        self.get_position = self.pos			
        self.get_radius = self.radius

    # if thrusters turned on, draw ship with flames. Otherwise, draw ship without flames.    
    def draw(self,canvas):
        if self.thrust:
            thrust_image_center = (self.info.center[0] + self.info.size[0], self.info.center[1])
            canvas.draw_image(self.image, thrust_image_center, self.image_size, (self.pos[0], self.pos[1]), self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, (self.pos[0], self.pos[1]), self.image_size, self.angle)

    def shoot(self):
        global missile_group
        
        # initialize a_missile 
        a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)
        
        # a_missile position update
        a_missile.pos[0] = self.pos[0] + (self.radius * math.cos(self.angle))
        a_missile.pos[1] = self.pos[1] + (self.radius * math.sin(self.angle))
        
        # a_missile velocity update
        a_missile.vel[0] = self.vel[0] + angle_to_vector(self.angle)[0] * 5
        a_missile.vel[1] = self.vel[1] + angle_to_vector(self.angle)[1] * 5
        
        # play missile sound
        missile_sound.play()
        
        # add a_missile to missile_group
        missile_group.add(a_missile)

    def update(self):
        # position update
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # friction update
        c = .03 # c constant (can be any c consant less than 1)
        self.vel[0] *= (1 - c)
        self.vel[1] *= (1 - c)
        
        # thrust update
        forward = angle_to_vector(self.angle)
        if self.thrust:
            self.vel[0] += forward[0] * .25
            self.vel[1] += forward[1] * .25
            
        # ship orientation update
        self.angle += self.angle_vel
      
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()   
        self.get_position = self.pos		
        self.get_radius = self.radius
   
    # if collision, return True. else, return False
    def collide(self, other_object):
        d = dist(self.get_position, other_object.get_position)
        if d > (self.get_radius + other_object.get_radius):
            return False
        else:
            return True
    
    def draw(self, canvas):
        if self.animated:
            explosion_index = (self.age % self.lifespan) // 1
            canvas.draw_image(self.image, [self.image_center[0] + explosion_index * self.image_size[0], self.image_center[1]], self.image_size, self.pos, self.image_size)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # increment age by 1 sprite every time update is call
        self.age += .8
        
# mouseclick handlers that reset UI and conditions whether splash image is drawn
def click(pos):
    global started, lives, score
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2 < pos[0] < center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2 < pos[1] < center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        soundtrack.play()
        score = 0
        lives = 3
        started = True
        timer.start()

def draw(canvas):
    global time, started, lives, score, rock_group, missile_group
   
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
   
    # draw lives and score
    canvas.draw_text("Lives", ((WIDTH * .05, HEIGHT * .08)), 25, 'White')
    canvas.draw_text(str(lives), ((WIDTH * .05, HEIGHT * .12)), 25, 'White')
    canvas.draw_text("Score", ((WIDTH *.88, HEIGHT * .08)), 25, 'White')
    canvas.draw_text(str(score), ((WIDTH * .88, HEIGHT * .12)), 25, 'White')
    
    # draw ship
    my_ship.draw(canvas)
    
    if started:
        # update ship position
        my_ship.update()
        
        # draw and update rock_group and missile_group
        process_sprite_group(canvas, rock_group)
        process_sprite_group(canvas, missile_group)
        group_group_collide(missile_group, rock_group)
        process_sprite_group(canvas, explosion_group)
    
        # if ship collides with rock, removes rock from rock_group and decreases lives by 1
        if group_collide(rock_group, my_ship):
            lives -= 1

            # restart game when lives run out
            if lives < 1:
                timer.stop()
                lives = 0
                for rock in rock_group:
                    rock_group.remove(rock)
                for missile in missile_group:
                    missile_group.remove(missile)
                for explosion in explosion_group:
                    explosion_group.remove(explosion)
                soundtrack.pause()
                soundtrack.rewind()
                started = False
               
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
            
# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
    
    # initialize rock sprite with random position on canvas and random spin direction
    a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [.3, .4], 0, .1, asteroid_image, asteroid_info)
    a_rock.pos[0] = random.randrange(0, WIDTH) 
    a_rock.pos[1] = random.randrange(0, HEIGHT)       
    a_rock.vel[0] = random.randrange(0, 10) / 10.0
    a_rock.vel[1] = random.randrange(0, 10) / 10.0
    
    # random spinning direction of a_rock
    def random_spin_dir():
        return random.choice(["clockwise", "counter"])
    if random_spin_dir() == "counter":
        a_rock.angle_vel = -1 * a_rock.angle_vel
    
    # add rock sprite to rock_group set if there's 12 or less rocks on canvas 
    # AND if a_rock doesn't automatically collide with my_ship
    if (len(rock_group) <= 12 
        and dist(a_rock.get_position, my_ship.get_position) > (a_rock.get_radius + 1.2 * my_ship.get_radius)):
        rock_group.add(a_rock)
    
# initialize keydown and keyup handlers
def key_down_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel -= .075
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel += .075
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = True
        ship_thrust_sound.play()
    elif key == simplegui.KEY_MAP['space']:
        my_ship.shoot()
            
def key_up_handler(key):
    if key == simplegui.KEY_MAP['left']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['right']:
        my_ship.angle_vel = 0
    elif key == simplegui.KEY_MAP['up']:
        my_ship.thrust = False
        ship_thrust_sound.pause()
        ship_thrust_sound.rewind()
     
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set([])
missile_group = set([])
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
# timer.start()
frame.start()
