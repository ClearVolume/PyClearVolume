# pyclearvolume

python bindings to the [ClearVolume project](https://bitbucket.org/clearvolume/clearvolume) that enables serving numpy data from within python to the renderer.  

## Prerequisites

A working installation of [ClearVolume](https://bitbucket.org/clearvolume/clearvolume).


## Installing


Either via pip

> pip install git+http://bitbucket.org/clearvolume/pyclearvolume

or classically

> git clone http://bitbucket.org/clearvolume/pyclearvolume

> cd pyclearvolume

> python setup.py install


to test if everything worked just run from the command line   

> python -m pyclearvolume

which will serve some dummy data to the default port (9140 on localhost) ClearVolume is listening to. After that you can open the ClearVolume client and should see some colorful volumes popping up. 


## Usage

To create a instance of the data server just do 

    :::python 
	d = pyclearvolume.DataServer(
	    address = "localhost",
		port = 9140,
		maxVolumeNumber = 20,
        dropVolumeOnFull = True)

then start the server

	:::python
	d.start()

and send some data

	:::python
	d.sendData(data, time = 0, channel = 1, color ="1.0 0.4 0.2 1.0") 



###Example 


    ::python
	import numpy as np
	import time

	import pyclearvolume

	print "creating the server"

	d = pyclearvolume.DataServer(maxVolumeNumber=20)

	print "starting the server"

	d.start()

	print "starting to serve data"

	N = 128
	data = np.linspace(0,65000,N**3).reshape((N,)*3).astype(np.uint16)

	t = 0
	while True:
    	  args = {}
		  args["color"] = "%s %s %s 1."%tuple([str(c) for c in np.random.uniform(0,1,3)])
    	  args["voxelwidth"] = np.random.uniform(.2,1.6)
    	  args["voxelheight"] = np.random.uniform(.2,1.6)
    	  args["voxeldepth"] = np.random.uniform(.2,1.6)
    	  args["index"] = t

    	  print "sending..."
    	  
    	  d.sendData(data,**args)
    	  time.sleep(2)
    	  t += 1
