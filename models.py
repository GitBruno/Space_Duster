from defines import *
from pygame.math import Vector2
from utilis import wrap_ground, get_random_position

class GameObject:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity

    def move(self):
        self.position = wrap_ground(self.position + self.velocity)

class s_Spaceship(GameObject):
    MANEUVERABILITY = 3
    ACCELERATION = 0.02
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
        if(self.velocity[0] >= self.ACCELERATION):
            self.velocity = (self.velocity[0]-self.ACCELERATION,self.velocity[1]) 
        if(self.velocity[1] >= self.ACCELERATION):
            self.velocity = (self.velocity[0],self.velocity[1]-self.ACCELERATION) 
        if(self.velocity[0] <= self.ACCELERATION):
            self.velocity = (self.velocity[0]+self.ACCELERATION,self.velocity[1]) 
        if(self.velocity[1] <= self.ACCELERATION):
            self.velocity = (self.velocity[0],self.velocity[1]+self.ACCELERATION) 

        if( (self.velocity[0] < 0.001) and (self.velocity[0] > -0.001) ):
            self.velocity = (0,self.velocity[1])
        if( (self.velocity[1] < 0.001) and (self.velocity[1] > -0.001) ):
            self.velocity = (self.velocity[0],0)

class s_Bullet(GameObject):
    moves = 60
    def move(self):
        self.moves = self.moves-1
        self.position = wrap_ground(self.position + self.velocity)
