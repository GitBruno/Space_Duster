import random, math
from defines import *
from pygame import Color, image, mixer
from pygame.math import Vector2

def new_object_id():
    global OBJECT_COUNTER, MAX_OBJECTS
    OBJECT_COUNTER = (OBJECT_COUNTER + 1)%MAX_OBJECTS
    return OBJECT_COUNTER

def trunc(num):
    return num # float(('%.12f' % num).rstrip('0').rstrip('.'))

def get_image_path(name):
    return f"assets/sprites/{name}.png"

def load_sprite(name, with_alpha=True):
    loaded_sprite = image.load(get_image_path(name))
    if with_alpha:
        return loaded_sprite.convert_alpha()
    else:
        return loaded_sprite.convert()

def wrap_ground(position):
    return Vector2(
        position[0] % GROUND_SIZE, 
        position[1] % GROUND_SIZE
    )

def get_random_position():
    return Vector2(
        random.randrange(GROUND_SIZE),
        random.randrange(GROUND_SIZE)
    )

def get_random_velocity(min_speed, max_speed):
    speed = random.uniform(min_speed, max_speed)
    angle = random.randrange(0, 360)
    return Vector2(speed, 0).rotate(angle)

def get_random_direction(start_dir, max_displacement):
    direction = start_dir.copy()
    direction.rotate_ip(random.uniform(-max_displacement, max_displacement))
    return direction

def load_sound(name):
    path = f"assets/sounds/{name}.wav"
    return mixer.Sound(path)

def infinityBlit(sprite, blit_position, toSurface):
    # Draw with 8 inifinity tiles
    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (GROUND_SIZE,-GROUND_SIZE)))))
    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (GROUND_SIZE, 0)))))
    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (GROUND_SIZE, GROUND_SIZE)))))

    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (0,-GROUND_SIZE)))))
    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (0, GROUND_SIZE)))))

    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (-GROUND_SIZE,-GROUND_SIZE)))))
    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (-GROUND_SIZE, 0)))))
    toSurface.blit(sprite, tuple(map(sum, zip(blit_position, (-GROUND_SIZE, GROUND_SIZE)))))

    toSurface.blit(sprite, blit_position)

def getDistance(p1,p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def getGroundMargin(position):
    return {
        "top": position[1], 
        "right": GROUND_SIZE - position[0],
        "bottom": GROUND_SIZE - position[1],
        "left": position[0]
    }

def getInfinityDistance(p1, p2):
    p1_normal  = Vector2(p1[0]+GROUND_SIZE,p1[1]+GROUND_SIZE)
    p2_normal  = Vector2(p2[0]+GROUND_SIZE,p2[1]+GROUND_SIZE)

    top_left   = getDistance(p1_normal, p2)
    top_cent   = getDistance(p1_normal, (p2_normal[0],p2[1]) )
    top_right  = getDistance(p1_normal, (p2_normal[0]+GROUND_SIZE,p2[1]) )

    cent_left  = getDistance(p1_normal, (p2[0],p2_normal[1]) )
    cent_cent  = getDistance(p1_normal, p2_normal)
    cent_right = getDistance(p1_normal, (p2_normal[0]+GROUND_SIZE,p2_normal[1]))

    bot_left   = getDistance(p1_normal, (p2[0], p2_normal[1]+GROUND_SIZE) )
    bot_cent   = getDistance(p1_normal, (p2_normal[0], p2_normal[1]+GROUND_SIZE) )
    bot_right  = getDistance(p1_normal, (p2_normal[0]+GROUND_SIZE, p2_normal[1]+GROUND_SIZE) )

    return min(top_left,top_cent,top_right,cent_left,cent_cent,cent_right,bot_left,bot_cent,bot_right)

def blit_text(surface, text, font, offset=(0,0), color=Color("white")):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect()
    rect.center = Vector2(surface.get_size()) / 2
    rect.center = tuple(map(sum, zip( rect.center, offset)))
    surface.blit(text_surface, rect)

def updateScore(score):
    f = open('scores.txt','r')
    file = f.readlines()
    last = int(file[0])

    if last < int(score):
        f.close()
        file = open('scores.txt', 'w')
        file.write(str(score))
        file.close()

    return last
