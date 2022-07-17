import random
from defines import *
from pygame import Color, image, mixer
from pygame.math import Vector2

def trunc(num):
    return float(('%.6f' % num).rstrip('0').rstrip('.'))

def get_image_path(name):
    path = f"assets/sprites/{name}.png"
    return path

def load_sprite(name, with_alpha=True):
    path = f"assets/sprites/{name}.png"
    loaded_sprite = image.load(path)
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

