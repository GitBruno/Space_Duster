import sys
from defines import *
from dustclient import DustClient

if len(sys.argv) == 2:
    SERVER_ADDRESS = sys.argv[1]

client = DustClient(SERVER_ADDRESS)
client.board.loop()
