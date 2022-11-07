from math import floor
import random
from defines import *
from pygame.math import Vector2
from pygame.transform import rotozoom
from utilis import *
from spritesheet import SpriteSheet

class GameObject:
    def __init__(self, ownerid, objectid, sprite, 
                 position=Vector2(MID_GROUND,MID_GROUND),
                 velocity=Vector2(0, 0),
                 direction=Vector2(0, -1)):
        self.ownerid   = ownerid
        self.objectid  = objectid
        self.position  = Vector2(position)
        self.direction = Vector2(direction)
        self.velocity  = Vector2(velocity)
        self.sprite    = sprite
        self.width  = self.sprite.get_width()
        self.height = self.sprite.get_height()
        self.radius = self.width*0.5

    def update(self, position):
        self.position = position

    def move(self):
        self.position = wrap_ground(self.position + self.velocity)

    def collides_with(self, other_obj):
        return self.position.distance_to(other_obj.position) < self.radius + other_obj.radius

    def draw(self, surface):
        blit_position = self.position - (self.radius,self.radius)
        infinityBlit(self.sprite, blit_position, surface)

    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.velocity[0]),
                 trunc(self.velocity[1])]

class Spaceship(GameObject):
    deadsound = load_sound("bangLarge")
    def __init__(self, ownerid, sprites, position=get_random_position(), velocity=Vector2(0, 0), direction=Vector2(0, -1), thruster=0, shield=0, dead=0, score=0, highScore=0):
        super().__init__(ownerid, new_object_id(), sprites[0], position, velocity, direction)
        self.dead      = dead
        self.alpha     = 255
        self.thruster  = thruster
        self.shield    = shield
        self.score     = score
        self.highScore = highScore
        self.width     = self.sprite.get_width()
        self.height    = self.sprite.get_height()
        self.radius    = self.width*0.5
        self.sprite_thrust = sprites[1]
        self.sprite_shield = sprites[2]
        self.ss_explosion  = sprites[3]
        self.explframes    = []
        for i in range(7):
            self.explframes.append(self.ss_explosion.image_at((i*41,0,41,41)))
        self.currentFrame  = 0

    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        self.direction.rotate_ip(SHIP_MANEUVERABILITY * sign)

    def accelerate(self):
        self.velocity += self.direction * SHIP_ACCELERATION
        if( self.velocity[0] >  SHIP_MAX_SPEED):
            self.velocity[0] =  SHIP_MAX_SPEED
        if( self.velocity[0] < -SHIP_MAX_SPEED):
            self.velocity[0] = -SHIP_MAX_SPEED
        if( self.velocity[1] >  SHIP_MAX_SPEED):
            self.velocity[1] =  SHIP_MAX_SPEED
        if( self.velocity[1] < -SHIP_MAX_SPEED):
            self.velocity[1] = -SHIP_MAX_SPEED
        
        self.thruster = True

    def slow_down(self, deceleration=SHIP_DECELERATION):

        if(self.velocity[0] > SHIP_MIN_SPEED):
            self.velocity[0] -= deceleration
        elif(self.velocity[0] < -SHIP_MIN_SPEED):
            self.velocity[0] += deceleration
        elif(self.velocity[0] > 0):
             self.velocity[0] = SHIP_MIN_SPEED
        else:
            self.velocity[0] = -SHIP_MIN_SPEED

        if(self.velocity[1] > SHIP_MIN_SPEED):
            self.velocity[1] -= deceleration
        elif(self.velocity[1] < -SHIP_MIN_SPEED):
            self.velocity[1] += deceleration
        elif(self.velocity[1] > 0):
             self.velocity[1] = SHIP_MIN_SPEED
        else:
            self.velocity[1] = -SHIP_MIN_SPEED

    def update(self, position, direction, thruster, shield, dead, score, highScore):
        self.position = position
        self.direction = direction
        self.thruster = thruster
        self.shield = shield
        self.dead = dead
        self.score = score
        self.highScore = highScore

    def draw(self, toSurface):
        if self.dead == 2:
            return
        if self.dead == 1:
            self.velocity = (0,0)
            angle = self.direction.angle_to(Vector2(0,-1))
            rotated_surface = rotozoom(self.explframes[int(self.currentFrame)], angle, 1.0)
            rotated_surface_size = Vector2(rotated_surface.get_size())
            blit_position = self.position - rotated_surface_size*0.5
            infinityBlit(rotated_surface, blit_position, toSurface)
            if self.currentFrame == 0:
                channel1.play(self.deadsound)
            self.currentFrame+=0.15
            if self.currentFrame >= 6:
                self.dead = 2
                self.currentFrame = 0
        else:
            angle = self.direction.angle_to(Vector2(0,-1))

            if self.shield:
                rotated_surface = rotozoom(self.sprite_shield, angle, 1.0)
                rotated_surface_size = Vector2(rotated_surface.get_size())
                blit_position = self.position - rotated_surface_size*0.5
                infinityBlit(rotated_surface, blit_position, toSurface)
                
            if self.thruster:
                rotated_surface = rotozoom(self.sprite_thrust, angle, 1.0)
            else:
                rotated_surface = rotozoom(self.sprite, angle, 1.0)

            rotated_surface_size = Vector2(rotated_surface.get_size())
            blit_position = self.position - rotated_surface_size*0.5
            infinityBlit(rotated_surface, blit_position, toSurface)

    def getData(self):
        self.slow_down(SHIP_DRAG)
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.direction[0]), 
                 trunc(self.direction[1]),
                 self.thruster, self.shield,
                 self.dead, self.score, self.highScore]

class Bullet(GameObject):
    def __init__( self, ownerid, objectid, sprite,
                  position=Vector2(MID_GROUND,MID_GROUND), 
                  direction=Vector2(0, -1)
                ):
        super().__init__(ownerid, objectid, sprite, position, direction)
        self.touched = False

    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.velocity[0]),
                 trunc(self.velocity[1])]

class Asteroid(GameObject):
    # It might be quicker to save the spritesheet for all and draw at scale
    def __init__(self, objectid, sprite_sheet, debri_sprite, position, direction, add_asteroid_callback, debri_arr, size=3):
        self.size = size
        self.playSpeed = random.choice([0.125,0.25,0.5])
        size_to_scale = {
            3: 0.7  + random.uniform(0, 0.3),
            2: 0.5  + random.uniform(0, 0.3),
            1: 0.25 + random.uniform(0, 0.3)}
        self.sprite_sheet = sprite_sheet
        self.debri_sprite = debri_sprite
        self.frames = []
        for y in range(8):
            for x in range(8):
                sy = y*95
                sx = x*95
                self.frames.append(rotozoom(sprite_sheet.image_at((sx,sy,95,95)), 0, size_to_scale[size]).convert_alpha())


        self.currentFrame = 0
        self.framemod = random.randint(0,1)

        super().__init__(0, objectid, self.frames[(32*self.framemod)+int(self.currentFrame)], position, get_random_velocity(0.25, 1.75))
        self.add_asteroid = add_asteroid_callback
        self.debri_arr = debri_arr

    def update(self, position):
        self.position = position

    def split(self):
        if self.size > 1:
            for _ in range(random.randint(2,4)):
                if(len(self.debri_arr) > MAX_DEBRI):
                    return
                _id = new_object_id()
                self.add_asteroid({_id : Asteroid(_id, self.sprite_sheet, self.debri_sprite, self.position, self.direction, self.add_asteroid, self.debri_arr, self.size - 1) } )

    def hit(self):
        for dust in range (random.randint(self.size * 10, self.size * 30)):
            self.debri_arr.append(Debri(self.ownerid, self.debri_sprite, self.position, get_random_velocity(0.5, 2.5), get_random_direction(self.direction, PARTICLE_ANGLE_WIDTH) ))

    def draw(self, surface):
        super().draw(surface)
        self.sprite = self.frames[(32*self.framemod)+int(self.currentFrame)]
        self.currentFrame += self.playSpeed
        if self.currentFrame >= 32:
            self.currentFrame = 0

    def getData(self):
        return [ self.ownerid, self.objectid, 
                 trunc(self.position[0]),
                 trunc(self.position[1]),
                 trunc(self.velocity[0]),
                 trunc(self.velocity[1]),
                 self.size]

class Debri(GameObject):
    def __init__(self, ownerid, debri_sprite, position, velocity, direction):
        self.moves = random.randint(20,60)
        super().__init__(ownerid, new_object_id(), debri_sprite, position, velocity, direction)

    def move(self):
        self.moves = self.moves-1
        self.position = wrap_ground(self.position + self.velocity)
