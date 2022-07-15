import socket, threading, msgpack
from defines import *
from game import Game

class DustServer:
    rSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    def __init__(self):
        self.sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rSocket.bind(("",SERVER_PORT))
        self.rThread = threading.Thread(target=self.receive, name="receive_thread")
        self.rThread.start()
        self.game = Game(self.send)
        print("Game Server Started...")

    def send(self, message, client_address=False):
        if client_address:
            self.unicast(client_address, message)
        else:
            self.broadcast(message)

    def unicast(self, client_address, message):
        self.sSocket.sendto(msgpack.packb(message), (client_address, CLIENT_PORT))

    def broadcast(self, message):
        self.sSocket.sendto(msgpack.packb(message), ('<broadcast>', CLIENT_PORT))

    def receive(self):
        while True:
            data, address = self.rSocket.recvfrom(BUFFERSIZE)
            self.game.handle_input(msgpack.unpackb(data),address)

