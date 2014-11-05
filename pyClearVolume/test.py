import socket
import numpy as np
import sys
import time



from data_utils import package_data


if __name__ == "__main__":


    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 9140)
    print 'starting up on %s port %s' % server_address

    try:
        sock.bind(server_address)
    except Exception as e:
        print e
        print "whooo"

    sock.listen(1)

    Ns = [111,122,133]

    d = (np.linspace(0,256,np.prod(Ns))).reshape(Ns).astype(np.uint8)


    dStr = package_data(d)

    while True:
        conn, addr = sock.accept()
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        while True:
            print "sending"
            conn.send(dStr)
            time.sleep(2)

    s.close()
