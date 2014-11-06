import socket


if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9140)
    sock.connect(server_address)

    while True:
        s = sock.recv(1024)
        print s
