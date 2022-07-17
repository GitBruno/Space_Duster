from math import floor
import random
from defines import *
from pygame.math import Vector2
from pygame.transform import rotozoom
from utilis import wrap_ground, get_random_position, infinityBlit, load_sprite, trunc

class s_GameObject:
    def __init__(self, ownerid, position, velocity):
        self.ownerid  = ownerid
        self.position = position
        self.velocity = velocity

    def move(self):
        self.position = wrap_ground(self.position + self.velocity)

    def getData(self):
        return [ self.ownerid, 
                 trunc(self.position[0]),
                 trunc(self.position[1])]

class c_GameObject:
    def __init__(self, position):
        self.position = position
        self.width  = 0
        self.height = 0
        self.radius = 0
        self.sprite = 0

    def draw(self, toSurface):
        blit_position = self.position - (self.radius,self.radius)
        infinityBlit(self.sprite, blit_position, toSurface)

class s_Spaceship(s_GameObject):
    MANEUVERABILITY = 0.1
    ACCELERATION = 0.002
    BULLET_SPEED = 3

    def __init__(self, ownerid):
        self.ownerid   = ownerid
        self.position  = get_random_position()
        self.velocity  = Vector2(0, 0)
        self.direction = Vector2(0, -1) #up
        self.alpha     = 255
        self.thruster  = False

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
        self.thruster = True
    
    def slow_down(self):
        DEAC = self.ACCELERATION*0.25
        if(self.velocity[0] >= self.ACCELERATION):
            self.velocity = (self.velocity[0]-DEAC,self.velocity[1]) 
        if(self.velocity[1] >= self.ACCELERATION):
            self.velocity = (self.velocity[0],self.velocity[1]-DEAC) 
        if(self.velocity[0] <= self.ACCELERATION):
            self.velocity = (self.velocity[0]+DEAC,self.velocity[1]) 
        if(self.velocity[1] <= self.ACCELERATION):
            self.velocity = (self.velocity[0],self.velocity[1]+DEAC) 

        if( (self.velocity[0] < 0.001) and (self.velocity[0] > -0.001) ):
            self.velocity = (0,self.velocity[1])
        if( (self.velocity[1] < 0.001) and (self.velocity[1] > -0.001) ):
            self.velocity = (self.velocity[0],0)
    
    def getData(self):
        return [ self.ownerid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 self.alpha,
                 self.thruster, 
                 trunc(self.direction[0]), 
                 trunc(self.direction[1])]

class c_Spaceship(c_GameObject):
    def __init__(self, id, position, direction, thruster=0, alpha=0):
        self.id = id
        self.position = position
        self.direction = direction
        self.alpha = alpha
        self.thruster = thruster
        self.sprite_thrust = load_sprite("spaceship_thrust")
        self.sprite = load_sprite('spaceship')
        self.width  = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.radius = self.width*0.5

    def update(self, position, direction, thruster):
        self.position = position
        self.direction = direction
        self.thruster = thruster
        if self.alpha <= 250:
            self.alpha = self.alpha + 5

    def draw(self, toSurface):
        angle = self.direction.angle_to(Vector2(0,-1))

        if self.thruster:
            rotated_surface = rotozoom(self.sprite_thrust, angle, 1.0)
        else:
            rotated_surface = rotozoom(self.sprite, angle, 1.0)

        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size*0.5        
        infinityBlit(rotated_surface, blit_position, toSurface)


class s_Bullet(s_GameObject):
    moves = random.randrange(60, 120)
    def move(self):
        self.moves = self.moves-1
        self.position = wrap_ground(self.position + self.velocity)

class c_Bullet(c_GameObject):
    def __init__(self, ownerid, position):
        self.ownerid = ownerid
        self.position = position
        self.sprite = load_sprite('bullet')
        self.width = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.radius = self.width*0.5
