import socket
import numpy as np
import sys
import time
import signal


from _serialize import _serialize_data



if __name__ == "__main__":


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ("localhost", 9141)
    print 'starting up on %s port %s' % server_address

    try:
        sock.bind(server_address)
    except Exception as e:
        print e

    sock.listen(10)

    # Ns = [3,4,5]

    # d = (np.linspace(0,256,np.prod(Ns))).reshape(Ns).astype(np.uint8)


    # dStr = package_data(d)

    def exit_handler(signum, frame):
        print "closing"
        sock.close()

    signal.signal(signal.SIGINT,exit_handler)

    conn, addr = sock.accept()
    print 'Connected with ' + addr[0] + ':' + str(addr[1])
    # while True:
    #     print "sending"

    #     d = (np.linspace(0,np.random.randint(100,256),np.prod(Ns))).reshape(Ns).astype(np.uint8)
    #     dStr = package_data(d)

    #     conn.send(dStr)
    #     time.sleep(1)

    sock.close()
