import socket, threading, msgpack
from defines import *
from board import Board

class DustClient:
    rSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self, server_address, screen):
        self.server_address = server_address
        self.board = Board(self.send, screen)
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rSocket.bind(("", CLIENT_PORT))
        self.rThread = threading.Thread(target=self.receive, name="receive_loop")
        self.rThread.start()

    def receive(self):
        while True:
            data, address = self.rSocket.recvfrom(BUFFERSIZE)
            self.board.update(msgpack.unpackb(data))

    def send(self, message):
        self.sSocket.sendto(msgpack.packb(message), (self.server_address, SERVER_PORT))
