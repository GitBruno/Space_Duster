import sys, socket, threading, msgpack

from defines import *

import time

if len(sys.argv) == 2:
    SERVER_ADDRESS = sys.argv[1]

class DustClient:
    rSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def __init__(self):
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.rSocket.bind(("", CLIENT_PORT))
        self.rThread = threading.Thread(target=self.receive, name="receive_loop")
        self.rThread.daemon = True
        self.rThread.start()

    def receive(self):
        while True:
            data, address = self.rSocket.recvfrom(BUFFERSIZE)
            print(msgpack.unpackb(data)[0],address)

    def send(self, message):
        self.sSocket.sendto(msgpack.packb(message), (SERVER_ADDRESS, SERVER_PORT))

client = DustClient()

def send_loop():
    while True:
        client.send(["Message", "for", "Server"])
        time.sleep(2)

test_thread = threading.Thread(target=send_loop, name="send_loop")
test_thread.start()
