import socket
import threading
import time

from defines import *

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
        #self.rThread.daemon = True
        self.rThread.start()
        print("Server Started...")

    def broadcast(self, message):
        self.sSocket.sendto(message, ('<broadcast>', CLIENT_PORT))

    def receive(self):
        while True:
            data, address = self.rSocket.recvfrom(1024)
            print(data, address)

server = DustServer()

def send_loop():
    while True:
        server.broadcast(b"Message for all clients")
        time.sleep(10)

test_thread = threading.Thread(target=send_loop, name="test_thread")
test_thread.start()
