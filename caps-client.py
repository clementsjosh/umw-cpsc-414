#!/usr/bin/python3

import socket

# the host we are connecting to and the port
HOST = "34.73.15.22"
PORT = 5220

# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect the socket to the server
sock.connect((HOST, PORT))

# get a string from the user
mesg = input("Enter a string: ")

# convert it to raw bytes
data = mesg.encode()

# send it to the server
sock.sendall(data)

# read the response
data = sock.recv(1024)

# convert it to a string
mesg = data.decode()

# print it out
print(mesg)

# and close the socket
sock.close() 

