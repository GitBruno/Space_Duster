import sys, socket, threading, time

SERVER_ADDRESS = "127.0.0.1"
SERVER_PORT = 44444
CLIENT_PORT = 37020

if len(sys.argv) == 2:
    SERVER_ADDRESS = sys.argv[1]

rSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
rSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
rSocket.bind(("", CLIENT_PORT))

sSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP

def receive_loop():
    while True:
        data, address = rSocket.recvfrom(1024)
        print(data)

def send():
    while True:
        sSocket.sendto(b"Message for Server", (SERVER_ADDRESS, SERVER_PORT))
        time.sleep(2)

send_thread = threading.Thread(target=send, name="send_loop")
#send_thread.daemon = True
send_thread.start()

receive_thread = threading.Thread(target=receive_loop, name="receive_loop")
receive_thread.start()
