#!/usr/bin/python3

import socket

# open the file and read our value of Pi
f = open("pi.txt", "r")
pi = f.read()

# TODO - put in these values
HOST = ""
PORT = 0

# create our UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# send the request to the server
print("Sending the request...")
sock.sendto(b"pi", ((HOST, PORT)))

print("Receiving Pi...", end="")

# keep track of our version of pi
received = ""

# receive the digits of pi one by one
while True:
    digit, address = sock.recvfrom(1)
    digit = digit.decode()
    if digit == '-':
        break
    else:
        received = received + digit
sock.close()
print("Done!")

# TODO insert analysis code here



