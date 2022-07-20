from math import floor
import random
from defines import *
from pygame.math import Vector2
from pygame.transform import rotozoom
from utilis import wrap_ground, get_random_position, infinityBlit, load_sprite, trunc, new_object_id, get_random_velocity
from spritesheet import SpriteSheet

class s_GameObject:
    def __init__(self, ownerid, position, velocity):
        self.ownerid  = ownerid
        self.objectid = new_object_id()
        self.position = position
        self.velocity = velocity

    def move(self):
        self.position = wrap_ground(self.position + self.velocity)

    def collides_with(self, other_obj):
        return self.position.distance_to(other_obj.position) < self.radius + other_obj.radius

    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.velocity[0]),
                 trunc(self.velocity[1])]

class c_GameObject:
    def __init__(self, ownerid, objectid, sprite, position=Vector2(MID_GROUND,MID_GROUND), direction=Vector2(0, -1)):
        self.ownerid  = ownerid
        self.objectid = objectid
        self.position = position
        self.direction = direction
        self.sprite = sprite
        self.width  = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.radius = self.width*0.5

    def update(self, position):
        self.position = position

    def draw(self, surface):
        blit_position = self.position - (self.radius,self.radius)
        infinityBlit(self.sprite, blit_position, surface)
 
class s_Spaceship(s_GameObject):
    def __init__(self, ownerid):
        self.ownerid   = ownerid
        self.objectid = new_object_id()
        self.position  = get_random_position()
        self.velocity  = Vector2(0, 0)
        self.direction = Vector2(0, -1) #up
        self.alpha     = 255
        self.thruster  = False

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = SHIP_MANEUVERABILITY * sign
        self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity += self.direction * SHIP_ACCELERATION
        self.thruster = True
    
    def slow_down(self):
        DEAC = SHIP_ACCELERATION*0.25
        if(self.velocity[0] >= SHIP_ACCELERATION):
            self.velocity = (self.velocity[0]-DEAC,self.velocity[1]) 
        if(self.velocity[1] >= SHIP_ACCELERATION):
            self.velocity = (self.velocity[0],self.velocity[1]-DEAC) 
        if(self.velocity[0] <= SHIP_ACCELERATION):
            self.velocity = (self.velocity[0]+DEAC,self.velocity[1]) 
        if(self.velocity[1] <= SHIP_ACCELERATION):
            self.velocity = (self.velocity[0],self.velocity[1]+DEAC) 

        if( (self.velocity[0] < 0.001) and (self.velocity[0] > -0.001) ):
            self.velocity = (0,self.velocity[1])
        if( (self.velocity[1] < 0.001) and (self.velocity[1] > -0.001) ):
            self.velocity = (self.velocity[0],0)
    
    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.direction[0]), 
                 trunc(self.direction[1]),
                 self.thruster, self.alpha]

class c_Spaceship(c_GameObject):
    def __init__(self, ownerid, position, direction, thruster=0, alpha=0):
        self.ownerid = ownerid
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
    
    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.velocity[0]),
                 trunc(self.velocity[1]),
                 self.moves]


class c_Bullet(c_GameObject):
    def __init__( self, ownerid, objectid, sprite, moves,
                  position=Vector2(MID_GROUND,MID_GROUND), 
                  direction=Vector2(0, -1)
                ):
        super().__init__(self, ownerid, objectid, sprite, position, direction)
        self.moves  = moves

    def move(self):
        self.moves = self.moves-1
        super().move(self)

class s_Asteroid(s_GameObject):
    def __init__(self, position, add_asteroid_callback, size=3):
        super().__init__(0, position, get_random_velocity(0.5, 1.5))
        self.add_asteroid = add_asteroid_callback
        self.size = size

    def split(self):
        if self.size > 1:
            for _ in range(random.randint(2,4)):
                self.add_asteroid(s_Asteroid(self.position, self.add_asteroid, self.size - 1))

    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.velocity[0]),
                 trunc(self.velocity[1]),
                 self.size]


class c_Asteroid(c_GameObject):
    def __init__(self, objectid, sprite_sheet, position, direction, size=3):
        self.size = size
        size_to_scale = {
            3: 0.7  + random.uniform(0, 0.10),
            2: 0.5  + random.uniform(0, 0.05),
            1: 0.25 + random.uniform(0, 0.01)}

        super().__init__(0, objectid, rotozoom(sprite_sheet.image_at((0,0,95,95)), 0, size_to_scale[size]), position, get_random_velocity(0.1, 1))

        self.frames = []
        for y in range(8):
            for x in range(8):
                sy = y*95
                sx = x*95
                self.frames.append(rotozoom(sprite_sheet.image_at((sx,sy,95,95)), 0, size_to_scale[size]).convert_alpha())

        self.currentFrame = 0
        self.framemod = random.randint(0,1)

    def update(self, position):
        self.position = position

    def draw(self, surface):
        super().draw(surface)
        self.sprite = self.frames[(32*self.framemod)+int(self.currentFrame)]
        self.currentFrame += 0.25
        if self.currentFrame >= 32:
            self.currentFrame = 0
