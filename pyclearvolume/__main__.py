
import numpy as np
import time

import pyclearvolume

print "creating the server"

d = pyclearvolume.DataServer(maxVolumeNumber = 20)

print "starting the server"

d.start()

time.sleep(1)

print "starting to serve data"

Nsizes = np.linspace(128,512,4).astype(np.int)
Niter = 50


for Nsize in Nsizes:
    data = np.zeros((Nsize,)*3)
    print "sending data with size %s"%str(data.shape)
    for i in range(Niter):
        j = i%Nsize
        data[j,:,:] = 100
        d.sendData(data.astype(np.uint8), time = i)
        time.sleep(.01)
