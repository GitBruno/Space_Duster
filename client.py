import sys, pygame

from defines import *
from pygame.locals import *
from dustclient import DustClient

if len(sys.argv) == 2:
    SERVER_ADDRESS = sys.argv[1]

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Space Duster')
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

client = DustClient(SERVER_ADDRESS, screen)
client.board.loop()
