#!/usr/bin/python3

import socket

# host (internal) IP address and port
HOST = '10.128.0.2'
PORT = 4040

# main setup and loop body of the server
def main():
    # create the socket and let us rebind
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # set the socket host and port number up
    s.bind((HOST, PORT))
    s.listen()

    # wait for people to connect to the chat server
    while True:
        # accept a connection which has come through
        conn, addr = s.accept()
        print("Connection from:", addr)
        mesg = "The server thinks your IP is " + addr[0] + " and your port is " + str(addr[1]) + "."
        conn.sendall(mesg.encode())
        conn.close()

# launch the whole thang
main()



