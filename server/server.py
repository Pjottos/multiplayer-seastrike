import socket, select

from classes import *

connections = []
players = []
buffer = 4096
socket.setdefaulttimeout(5.0)

host, port = '127.0.0.1', 24568
hostsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('socket created')
try:
    hostsocket.bind((host, port))
except socket.error:
    print('binding to socket failed')

hostsocket.listen(5)
connections.append(hostsocket)
print('listening on socket')

curTurn = False

while 1:
    read_sockets, write_sockets, error_sockets = select.select(connections, [], [])

    for sock in read_sockets:
        if sock == hostsocket:
            client, addr = hostsocket.accept()
            connections.append(client)

            if len(connections) <= 3:
                print('new connection from (%s, %s), asking for nickname...' % addr)
                client.send(b'Choose a nickname')
                nick = client.recv(buffer).decode('utf-8')
                players.append(Player(addr, nick, client))
                print('(%s, %s) chose '+nick+' as nickname' % addr)
            else:
                connections.remove(client)
                client.close()
        else:
            data = sock.recv(buffer)
            data = data.decode('utf-8').split(':')
            instruction = data[0]

            if instruction == 'STRIKE':
                if sock == players[curTurn].sock:
                    players[not curTurn].sock.send(('TRY:'+data[1]).encode('utf-8'))
                    result = players[not curTurn].sock.recv(buffer)
                    if result == b'True':
                        sock.send(b'HIT')
                    else:
                        sock.send(b'MISS')
                        curTurn = not curTurn
            elif instruction == 'EXIT':
                sock.close()
                for player in players:
                    if player.sock == sock:
                        players.remove(player)
                        print(player.nick+' left')





