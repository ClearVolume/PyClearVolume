
from pyclearvolume.folder_watch_thread import WatchThread

import pyclearvolume
import numpy as np
import time


def prepare_data(data):
    """ensure data is a nice uint16 array"""
    if data.ndim != 3:
        raise ValueError("data has invalid dimensions (%s)"%(data.shape,))
    data = data.astype(np.uint16)
    return data

if __name__ == "__main__":

    d = pyclearvolume.DataServer(maxVolumeNumber=20)

    d.start()

    watchThread = WatchThread("/Users/mweigert/python/bioformats_test/data"
    )
    watchThread.start()

    t = 0
    while True:
        if d.is_connected() and not watchThread.empty():
            print "connected to %s %s"%(d.client_address())
            data = watchThread.get()
            print data
            try:
                data = prepare_data(data)
                args = {}
                args["index"] = t
                print "sending data of shape %s"%(data.shape,)
                d.sendData(data,**args)
                t += 1
            except  Exception as e:
                print e

        time.sleep(4.)


    
