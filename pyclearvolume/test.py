from pyclearvolume import DataServer, ImageFileReader

import numpy as np
import time

if __name__ == "__main__":

    data, meta = ImageFileReader.load_file("/Users/mweigert/Tmp/CVTmp/retina.czi")
    data = data[0,0,0,:,:,:,0]

    # data = np.linspace(0,255,64**3).reshape((64,)*3)
    
    d = DataServer(maxVolumeNumber=20)

    d.start()

    d.sendData(data.astype(np.uint8))

    d.serveUntilEmpty()

    
    # d.stop()


    # time.sleep(1.)
