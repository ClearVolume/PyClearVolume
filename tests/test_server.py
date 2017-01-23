from __future__ import print_function, division
from __future__ import absolute_import
import numpy as np
import time

import pyclearvolume



def test_server(dtype = np.uint8, N = 128):
    print("creating the server")

    d = pyclearvolume.DataServer(maxVolumeNumber=2)

    d.start()

    time.sleep(1)

    print("starting to serve data")

    typeinfo = np.iinfo(dtype)
    
    data = np.linspace(typeinfo.min,typeinfo.max,N**3).reshape((N,)*3).astype(dtype)

  
    t = 0
    while True:
        if d.is_connected():
            print("connected to %s %s"%(d.client_address()))
            args = {}
            args["color"] = "%s %s %s 1."%tuple([str(c) for c in np.random.uniform(0,1,3)])
            args["voxelwidth"] = np.random.uniform(.2,1.6)
            args["voxelheight"] = np.random.uniform(.2,1.6)
            args["voxeldepth"] = np.random.uniform(.2,1.6)
            args["index"] = t
            print("sending...")
            print(args)
            d.sendData(data,**args)
            t += 1

        # d.sendData(data)
        time.sleep(2)




if __name__ == '__main__':
    test_server(dtype = np.uint16)
