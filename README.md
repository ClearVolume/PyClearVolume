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


to test if everything worked, you should first start ClearVolume and then run from the command line   

> python -m pyclearvolume

which will serve some dummy data to the default port ClearVolume is listening to.


## Usage


    :::python 
	import pyclearvolume
	
	d = pyclearvolume.DataServer()

	d.start()

	d.sendData(data)  #without metadata
	
	d.sendData(data, time = 0, channel = 1)  #with metadata
    

The metadata fields currently supported by ClearVolume are

	:::python
	widthreal,
	elementsize,
	realunit,
	heightreal,
    index,
	depthreal,
	dim,
	bytespervoxel,
	time,
	type,
	channel