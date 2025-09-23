import select
import socket
import sys

HOST = 'localhost'
PORT = 12345

def run_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(False)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    inputs = [server_socket, sys.stdin]  # Monitor server socket and standard input
    print(f"Server listening on {HOST}:{PORT}")

    running = True
    while running:
        readable, _, _ = select.select(inputs, [], [], 0.1) # Timeout for responsiveness

        for sock in readable:
            if sock is server_socket:
                conn, addr = server_socket.accept()
                conn.setblocking(False)
                inputs.append(conn)
                print(f"Accepted connection from {addr}")
            elif sock is sys.stdin:
                command = sys.stdin.readline().strip()
                if command.lower() == 'quit':
                    print("Quit command received. Shutting down server.")
                    running = False
                else:
                    print(f"Unknown command: {command}")
            else:
                data = sock.recv(1024)
                if data:
                    message = data.decode().strip()
                    print(f"Received from {sock.getpeername()}: {message}")
                    sock.sendall(f"Server received: {message}".encode())
                else:
                    print(f"Closing connection from {sock.getpeername()}")
                    inputs.remove(sock)
                    sock.close()

    server_socket.close()
    print("Server shut down.")

if __name__ == "__main__":
    run_server()