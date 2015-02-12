import os
import time
import Queue
import threading
import numpy as np

from folder_watch_thread import WatchThread



class SlowlyFileWriteThread(threading.Thread):
    """
    simulates a slowly write of an image file 
    """
    def __init__(self,fName, timestep = .1, chunksize = 64):
        super(SlowlyFileWriteThread,self).__init__()
        self.fName = fName
        self.timestep = timestep
        self.chunksize = chunksize
        #erase file
        with open(self.fName,"w") as f:
            pass
        
        self.setDaemon(True)
    

    def run(self):
        while True:
            with open(self.fName,"a") as f:
                f.write("1"*self.chunksize)                
            time.sleep(self.timestep)



if __name__ == "__main__":

    dirName =  "tests_watch/"

    randName = "RANDOM_%d.tif"%(time.time())

    
    writeSimulator = SlowlyFileWriteThread(os.path.join(dirName,randName))

    writeSimulator.start()

    
    a = WatchThread(dirName, deltaTime = 1.)
    a.start()

    while True:
        try:
            fName = a.goodFiles.get(timeout = 1.)
            print "a new file arrived! ", fName
        except Queue.Empty:
            pass
        time.sleep(.1)

    
