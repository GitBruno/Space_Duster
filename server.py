import socket, threading, msgpack
from defines import *
from s_game import s_Game

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
        self.game = s_Game(self.send)
        print("Game Server Started...")

    def send(self, message, client_ip=False):
        if client_ip: # unicast
            self.sSocket.sendto(msgpack.packb(message), (client_ip, CLIENT_PORT))
        else: # broadcast
            self.sSocket.sendto(msgpack.packb(message), ('<broadcast>', CLIENT_PORT))

    def receive(self):
        while True:
            data, address = self.rSocket.recvfrom(BUFFERSIZE)
            self.game.handle_input(msgpack.unpackb(data),address)

server = DustServer()
server.game.loop()