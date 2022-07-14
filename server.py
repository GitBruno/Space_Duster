import socket
import threading
import time
 
SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 44444
CLIENT_PORT = 37020

# create sockets
rSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rSocket.bind(("",SERVER_PORT))

sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
sSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

message = b"Message for all clients"

def send(msg):
    sSocket.sendto(msg, ('<broadcast>', CLIENT_PORT))

def receive_loop():
    while True:
        data, address = rSocket.recvfrom(1024)
        print(data, address)

def send_loop():
    while True:
        send(message)
        print("message sent!")
        time.sleep(5)

send_thread = threading.Thread(target=send_loop, name="send_loop")
#send_thread.daemon = True
send_thread.start()

receive_thread = threading.Thread(target=receive_loop, name="receive_loop")
receive_thread.start()
