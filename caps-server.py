#!/usr/bin/python3

import socket
import select
import sys


# host (internal) IP address and port
HOST = "127.0.0.1"
PORT = 41400

# create our socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# allow us to reuse an address for restarts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# set the socket host and port number up
sock.bind((HOST, PORT))

# listen for any clients connecting
sock.listen()

print(f'Server running on {HOST}:{PORT}. Type "q" and press Enter to quit.')

running = True

while running:
    
    reads, writes, errors = select.select([sys.stdin, sock], [], [])

    for read in reads:
        if read is sys.stdin:
            user_input = sys.stdin.readline().strip()
            if user_input.lower()[0] == 'q':
                running = False
        elif read is sock:
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

sock.close()
print("Quitting... have a nice day.")
