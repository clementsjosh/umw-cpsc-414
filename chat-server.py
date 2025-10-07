#!/usr/bin/python3

import socket
import threading
import time
import select
import copy

# host (internal) IP address and port
HOST = 'localhost'
PORT = 41400

# the amount of time after sending messages to avoid jumblies
DELAY = 0.15

# a map of room names, to lists of users
# each user is a tuple (conn, 'nick')
new_clients = {}

# this is called when there is a name collision, the point is to find a new name!
def new_name_needed(person, room_name):
    print(person[0], "took a taken name in", room_name)
    person[1].send(b"2")
    # read their nick name until valid
    while True:
        nick = person[1].recv(1024).decode().rstrip().split(' ')
        if nick[0] == "/logout":
            print("User logged out when picking name")
            person[1].close()
            return
        if len(nick) != 2 or nick[0] != "/nick" or not nick[1].isalnum():
            person[1].send(b"1")
        else:
            # name is OK, but may be taken
            break

    new_person = (nick[1], person[1])
    # name is valid, try to send to the room again!
    new_clients[room_name].append(new_person)


# this function is called in 1 thread for each chat room
def handle_room(room):
    # put the room creator into a list of users
    users = []
    assert len(new_clients[room]) == 1
    users.append(new_clients[room][0])
    new_clients[room].clear()

    # send them name OK and an empty room message
    users[0][1].sendall(b"0")
    users[0][1].sendall(b"You have joined a new room.")

    # keep going while there are users in the room
    while True:
        try:
            # check if room has new users
            for person in new_clients[room]:
                print("Checking the name", person[0], "...", end="")
                # check if their name is taken!
                taken = False
                for peer in users:
                    if peer[0] == person[0]:
                        # the names match
                        print(" TAKEN!")
                        taken = True
                        thread = threading.Thread(target = new_name_needed, args = (person, room))
                        thread.start()
                if not taken:
                    print(" fine!")
                    person[1].send(b"0")
                    print("Adding", person[0], "to room", room)
                    users.append(person)
                    for peer in users:
                        try:
                            peer[1].sendall(person[0].encode() + b" has joined the room.  ")
                            peer[1].sendall(b"There are " + str(len(users)).encode() + b" people in the room.")
                        except BrokenPipeError:
                            users.remove(peer)
                            peer[1].close()
                            for p2 in users:
                                if p2[0] != peer[0]:
                                    p2[1].sendall(peer[0].encode() + b" has been disconnected.")
                else:
                    print("Somehow taken!")
            new_clients[room].clear()

            # check if anyone typed a new message
            for user in users:
                reads, writes, errs = select.select([user[1]], [], [], 0.25)
                for reader in reads:
                    mesg = user[1].recv(1024).rstrip()
                    print(user[0], " said '", mesg, "'.", sep = '')

                    # check if they want a list of users
                    if mesg == b"/who":
                        user[1].sendall(b"Users in this room:")
                        time.sleep(DELAY)
                        for r in users:
                            user[1].sendall(r[0].encode())
                            time.sleep(DELAY)

                    # check if it is the logout message
                    elif mesg == b"/logout" or mesg == b"":
                        users.remove(user)
                        print("Removing", user[0], "from room", room)
                        user[1].close()
                        for peer in users:
                            try:
                                peer[1].sendall(user[0].encode() + b" has left the room.")
                            except BrokenPipeError:
                                users.remove(peer)
                                peer[1].close()
                                for p2 in users:
                                    if p2[0] != peer[0]:
                                        p2[1].sendall(peer[0].encode() + b" has been disconnected.")

                    else:
                        # send it on to all of them
                        for peer in users:
                            if peer[0] != user[0]:
                                try:
                                    peer[1].sendall(user[0].encode() + b"> " + mesg)
                                except BrokenPipeError:
                                    users.remove(peer)
                                    peer[1].close()
                                    for p2 in users:
                                        if p2[0] != peer[0]:
                                            p2[1].sendall(peer[0].encode() + b" has been disconnected.")
        except:
            print("Thread for room", room, "had an exception, moving along!")

# this function is called in a thread once someone connects and we need their deets
def handle_new_client(conn, addr):
    try:
        # read their room to join until valid
        while True:
            print("Waiting for client to join...")
            response = conn.recv(1024).decode().rstrip()
            room = response.split(" ")
            print(room)

            if response == "/logout":
                print("User logged out when choosing room.")
                conn.close()
                return

            # if we receive /list, then we must list the rooms available
            elif response == "/list":
                print("Client got list")
                conn.sendall(str(len(new_clients)).encode())
                time.sleep(DELAY)
                for r in new_clients:
                    conn.sendall(r.encode())
                    time.sleep(DELAY)

            # else assume the tried to send a join message
            elif len(room) != 2 or room[0] != "/join" or not room[1].isalnum():
                print("Client messed up room named", room[1:])
                conn.sendall(b"1")
            else:
                print("Client joined", room[1])
                conn.sendall(b"0")
                break

        # read their nick name until valid
        while True:
            nick = conn.recv(1024).decode().rstrip().split(' ')
            if nick[0] == "/logout":
                print("User logged out when picking name")
                conn.close()
                return

            if len(nick) != 2 or nick[0] != "/nick" or not nick[1].isalnum():
                print("Client messed up nickname '", nick[1], "'", sep='')
                conn.send(b"1")
            else:
                print("Client is named", nick[1])
                # name is OK, but may be taken
                break

        # if the room has not been made yet, make it, and spawn a handler
        room_name = room[1]
        nick_name = nick[1]
        if not room_name in new_clients:
            print("Making new room", room_name, "for", nick_name)
            new_clients[room_name] = [(nick_name, conn)]
            thread = threading.Thread(target = handle_room, args = (room_name,))
            thread.start()
        else:
            # just add it to the list (append is thread safe in Python)
            new_clients[room_name].append((nick_name, conn))
    except:
        print("Client failed to join room...")
        return


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
        thread = threading.Thread(target = handle_new_client, args = (conn, addr))
        thread.start()

# launch the whole thang
main()



