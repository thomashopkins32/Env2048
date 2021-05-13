'''
server.py

Creates a TCP socket to communicate board states to AI agents.

Server can only receive 1 byte character with the following rules:

'N' - new game
'R' - right move
'L' - left move
'U' - up move
'D' - down move
'E' - end connection

Server sends state of game board in compressed form.

NOTE: Only works for 4x4 game boards
'''
import sys
import socket

from AI2048.game import GameState

MOVE_DICT = {'R': 'right', 'L': 'left', 'U': 'up', 'D': 'down'}

if len(sys.argv) != 2:
    print('ERROR: Invalid argument(s)\nUSAGE: python server.py <hostname> <port>')
    quit()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((sys.argv[1], int(sys.argv[2])))
s.listen()

# accept single connection
client, addr = s.accept()
game = None
# receive messages
while data != 'E':
    data = socket.ntohl(client.recv(1)).decode()
    print(f'Received: {data}')
    if data == 'N':
        game = GameState()
        client.sendto(socket.htonl(game.compact()), addr)
    elif data in MOVE_DICT.keys():
        game.move(MOVE_DICT[data])
        client.sendto(socket.htonl(game.compact()), addr)
    else:
        print('Unknown message')

client.close()
s.close()
print('Connection closed')
