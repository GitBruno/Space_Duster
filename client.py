import socket, threading, msgpack
import sys, pygame

from defines import *
from pygame.locals import *
from c_game import c_Game

if len(sys.argv) == 2:
    SERVER_ADDRESS = sys.argv[1]

pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption('Space Duster')
pygame.event.set_allowed([QUIT, KEYDOWN, KEYUP])

class DustClient:
    rSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, server_address, screen):
        self.server_address = server_address
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rSocket.bind(("", CLIENT_PORT))
        self.game = c_Game(self.send, screen)
        self.rThread = threading.Thread(target=self.receive, name="receive_loop")
        self.rThread.start()
        self.game.loop()

    def receive(self):
        while True:
            data, address = self.rSocket.recvfrom(BUFFERSIZE)
            self.game.update(msgpack.unpackb(data))

    def send(self, message):
        self.sSocket.sendto(msgpack.packb(message), (self.server_address, SERVER_PORT))

client = DustClient(SERVER_ADDRESS, screen)
