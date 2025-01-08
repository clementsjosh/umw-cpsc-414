#!/usr/bin/python3

import socket

# host (internal) IP address and port
HOST = "10.142.0.3"
PORT = 5220

# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us to reuse an address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set the socket host and port number up
sock.bind((HOST, PORT))

# listen for any clients connecting
sock.listen()

# wait for a client to connect to us
# accept a connection which has come through
conn, addr = sock.accept()
print("Connection from:", addr)

# read some bytes from the client
data = conn.recv(1024)

# decode it into a string
string = data.decode()

# convert it to uppercase
string = string.upper()

# now encode the data for sending back
data = string.encode()

# send it back
conn.sendall(data)

# and done
conn.close()

# done with listening on our socket to
sock.close()

