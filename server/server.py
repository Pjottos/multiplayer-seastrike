import socket, select

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

curTurn = 1

while 1:
    read_sockets, write_sockets, error_sockets = select.select(connections, [], [])

    for sock in read_sockets:
        if sock == hostsocket:
            client, addr = hostsocket.accept()
            connections.append(client)

            if len(connections) <= 3:
                print('new connection from (%s, %s), asking for nickname...' % addr)
                client.send(b'REQ_NICK')
                nick = client.recv(buffer).decode('utf-8')
                players.append((nick, addr))
                print('(%s, %s) chose '+nick+' as nickname' % addr)
            else:
                connections.remove(client)
                client.close()
        else:
            instruction, player = sock.recvfrom(buffer)




