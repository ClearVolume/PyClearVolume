



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
        
