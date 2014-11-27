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
logger.setLevel(logging.INFO)

######

__all__ = ["DataServer"]



class DataServer:
    """
    The main data serving object.

    Basic usage:


    d = DataServer()

    d.start()

    data = linspace(0,100,100**3).reshape((100,100,100))

    d.sendData(data.astype(uint16))


    """

    _DEFAULT_ADDRESS = ""
    _DEFAULT_PORT = 9140

    _TIMEOUT = .001

    FullQueueError = Exception("Data queue is full and policy was not set to drop!")

    def __init__(self,
                 address = _DEFAULT_ADDRESS,
                 port = _DEFAULT_PORT,
                 maxVolumeNumber = 20,
                 dropVolumeOnFull = True):

        self.sock = socket.socket()
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.dataQueue = Queue.Queue(maxsize = max(1,maxVolumeNumber))
        self.dataThread = _DataServerThread(self.sock, self.dataQueue)
        self.dropVolumeOnFull = dropVolumeOnFull
        self._bind(address,port)

    def _bind(self, address = _DEFAULT_ADDRESS, port = _DEFAULT_PORT):
        logger.debug("binding with address %s at port %s "%(address,port))
        try:
            self.sock.bind((address,port))
        except Exception as e:
            print e

        self.sock.listen(10)

    def sendData(self, data, **kwargs):
        """sends array data to the server

        data : a 3d uint16 numpy array

        supported keyword arguments with its defaults:

          "index":0,
          "time": 0,
          "channel": 0,
          "channelname": "python source",
          "color": "1. 1. 1. 1.",
          "viewmatrix": "1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.",
          "dim": 3,
          "type": "Byte",
          "bytespervoxel":1,
          "elementsize": 1,
          "voxelwidth": 1,
          "voxelheight": 1,
          "voxeldepth": 1,
          "realunit":1

        """

        logger.debug("got data of shape %s"%str(data.shape))
        logger.debug("meta: %s"%kwargs)

        if self.dataQueue.full():
            if self.dropVolumeOnFull:
                while self.dataQueue.full():
                    self.dataQueue.get(block=True,timeout = self._TIMEOUT)
            else:
                raise self.FullQueueError

        self.dataQueue.put((data, kwargs))

    def isConnected(self):
        return self.dataThread.isconnected

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
        self.isconnected = False



    def run(self):
        self.isRunning = True
        while self.isRunning:
            logger.debug("waiting for connection...")
            self.isconnected = False
            conn, addr = self.sock.accept()
            logger.debug("...connected!")
            self.isconnected = True

            logger.debug("now serving the data...")
            while True:
                try:
                    data, meta = self.dataQueue.get(block = True, timeout = self._TIMEOUT)
                    self.send_data(conn,data, meta)
                except Queue.Empty:
                    # logger.debug("no data :(")
                    pass
                except socket.error:
                    logger.debug("socket broken")
                    break

    def stop(self):
        # logger.debug("stopping thread")
        self.isRunning = False

    def send_data(self,conn,data, meta = {}):
        # print "SEEEEND ", data.shape, meta
        conn.send(_serialize_data(data, meta))
        #_serialize_data



def test_full():
    import numpy as np

    d = DataServer(maxVolumeNumber=2)
    d.start()
    data = np.zeros((10,)*3)

    d.sendData(data)
    d.sendData(data)
    d.sendData(data)



def test_serve_forever():
    import numpy as np
    import time

    d = DataServer(maxVolumeNumber=2)
    d.start()
    N = 128

    data = np.linspace(0,65000,N**3).reshape((N,)*3).astype(np.uint16)

    t = 0
    while True:
        args = {}
        args["color"] = "%s %s %s 1."%tuple([str(c) for c in np.random.uniform(0,1,3)])
        args["voxelwidth"] = np.random.uniform(.2,1.6)
        args["voxelheight"] = np.random.uniform(.2,1.6)
        args["voxeldepth"] = np.random.uniform(.2,1.6)
        args["time"] = t

        print "sending..."
        print args
        d.sendData(data,**args)
        # d.sendData(data)
        time.sleep(2)
        t += 1


if __name__ == '__main__':


    # test_full()


    test_serve_forever()
