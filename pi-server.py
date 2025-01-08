#!/usr/bin/python3

import socket

# host (internal) IP address and port
HOST = '10.142.0.3'
PORT = 4040

# open the file and read our value of Pi
f = open("pi.txt", "r")
pi = f.read()

# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# allow us to reuse an address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set the socket host and port number up
sock.bind((HOST, PORT))

# wait for a client to connect to us with the "pi" message
print("Waiting for a connection...")
request, address = sock.recvfrom(1024)
print("Sending pi to", address)

# send the digits of pi one by one
for digit in pi:
    sock.sendto(digit.encode(), address)

# send lots of the ending character (in case they are dropped)
for i in range(1000):
    sock.sendto(b"-", address)

print("Done!")

# close connections
sock.close()

