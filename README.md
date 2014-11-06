# pyclearvolume

python bindings to the [ClearVolume project](https://bitbucket.org/royerloic/clearvolume) that enables serving numpy data from within python to the renderer.  

## Prerequisites

A working installation of [ClearVolume](https://bitbucket.org/royerloic/clearvolume).


## Installing


Either via pip

> pip install --user git+http://mweigert@bitbucket.org/mweigert/pyclearvolume

or classically

> git clone git+http://mweigert@bitbucket.org/mweigert/pyclearvolume

> cd pyclearvolume

> python setup.py install


if everything works, you may test if everything is right by first starting the ClearVolume GUI and then run from the command line   

> python -m pyclearvolume



## Usage


    :::python 
	import pyclearvolume
	
	d = pyclearvolume.DataServer()

	d.bind()		

	d.start()

	d.sendData(data, time = 0, channel = 0)
    
