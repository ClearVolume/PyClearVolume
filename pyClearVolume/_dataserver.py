"""
the data server providing the main functionality

author: Martin Weigert
email: mweigert@mpi-cbg.de
"""

import socket
import Queue
import threading


from _serialize import _serialize_data



######   logging stuff
import logging
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
######



class DataServer:
    """
    """

    _DEFAULT_ADDRESS = "localhost"
    _DEFAULT_PORT = 9140

    _TIMEOUT = .001

    def __init__(self, maxVolumeNumber = 20):
        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dataQueue = Queue.Queue()
        self.maxVolumeNumber = max(1,maxVolumeNumber)
        self.dataThread = _DataServerThread(self.sock, self.dataQueue)

    def bind(self, address = _DEFAULT_ADDRESS, port = _DEFAULT_PORT):
        logger.debug("binding with address %s at port %s "%(address,port))
        try:
            self.sock.bind((address,port))
        except Exception as e:
            print e

        self.sock.listen(10)

    def sendData(self, data, **kwargs):
        logger.debug("sending data of shape %s"%str(data.shape))
        logger.debug("header: %s"%kwargs)

        if self.dataQueue.qsize()>=self.maxVolumeNumber:
            self.dataQueue.get(block=True,timeout = self._TIMEOUT)
        self.dataQueue.put((data, kwargs))


    def start(self):
        logger.debug("starting server")
        self.dataThread.start()

    def stop(self):
        self.dataThread.stop()
        self.sock.close()

    def __del__(self):
        self.stop()


class _DataServerThread(threading.Thread):
    """
    """
    _TIMEOUT = 0.001
    def __init__(self, sock, dataQueue):
        threading.Thread.__init__ (self)
        self.sock = sock
        self.dataQueue  = dataQueue
        self.daemon = True


    def run(self):
        self.isRunning = True
        while self.isRunning:
            logger.debug("waiting for connection...")

            conn, addr = self.sock.accept()
            logger.debug("...connected!")

            logger.debug("now serving the data...")
            while True:
                try:
                    data, header = self.dataQueue.get(block = True, timeout = self._TIMEOUT)
                    self.send_data(conn,data, header)
                except Queue.Empty:
                    # logger.debug("no data :(")
                    pass
                except socket.error:
                    logger.debug("socket broken")
                    break

    def stop(self):
        # logger.debug("stopping thread")
        self.isRunning = False

    def send_data(self,conn,data, header = {}):
        print "SEEEEND ", data.shape, header
        conn.send(_serialize_data(data, header))
        #_serialize_data



if __name__ == '__main__':

    import numpy as np
    import time


    d = DataServer(maxVolumeNumber = 20)

    d.bind()

    d.start()

    time.sleep(4)
    print "staaaaart"

    
    for i in range(100):
        data = np.zeros((128,)*3)
        j = i%30
        data[3*j:3*(j+1),:,:] = 100


        print np.mean(data)
        d.sendData(data.astype(np.uint8), time = i)
        time.sleep(.1)

    # d.sendData(np.zeros((5,)*3))

    # time.sleep(4)

    # d.close()
