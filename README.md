![GitHub Logo](/images/logo64.png)
# pyclearvolume      

Python bindings to the [ClearVolume project](http://clearvolume.github.io/).

With it you can either serve numpy data directly from within python to any running ClearVolume client or send/watch a folder via *pyclearvolume_serve* and serve its content to the client (making it useful e.g. for remote scopes)  

## Prerequisites

A working installation of [ClearVolume](http://clearvolume.github.io/).


## Installing


Either via pip

> pip install git+https://github.com/ClearVolume/pyclearvolume

or classically

> git clone https://github.com/ClearVolume/pyclearvolume

> cd pyclearvolume

> python setup.py install

to test if everything worked just run from the command line


> python -m pyclearvolume

which will serve some dummy data to the default port (9140 on localhost) ClearVolume is listening to. After that you can open the ClearVolume client and should see some colorful volumes popping up. 


## Usage

### standalone utility

Pyclearvolume comes with an executable script *pyclearvolume_serve* that provides a fast way to serve single files (tif or czi) or folder to the client renderer. It further allows to watch a folder for changes and stream any newly arriving data.
See the options for all available parameters:

```
pyclearvolume_serve [-h] [-a ADDRESS] [-p PORT] [-w] [-t DTIME]
                              [-u UNITS UNITS UNITS] [-c COLOR COLOR COLOR]
                              files [files ...]

serves 3d image files or folder to a clearvolume client
    
pyclearvolume_serve  myfile.tif

pyclearvolume_serve -u 1. 1. 2. -a remote.domain.com -p 9140 myfile.tif 

        

positional arguments:
  files                 image files or folder to send/watch (currently
                        supported: ['.tif', '.czi', '.tiff']

optional arguments:
  -h, --help            show this help message and exit
  -a ADDRESS, --address ADDRESS
                        address to bind to (default: )
  -p PORT, --port PORT  port to bind to (default: 9140)
  -w, --watch           watch folder (default: False)
  -t DTIME, --time DTIME
                        time in secs in watch mode to wait for file not having
                        changed (default: 1.0)
  -u UNITS UNITS UNITS, --units UNITS UNITS UNITS
                        relative units of voxels e.g. -u 1. 1. 2. (default:
                        [1.0, 1.0, 1.0])
  -c COLOR COLOR COLOR, --color COLOR COLOR COLOR
                        color rgb in 0..1 (default: [1.0, 1.0, 1.0])
```

### from within python 

To create a instance of the data server just do 
```python
d = pyclearvolume.DataServer(
	address = "localhost",
	port = 9140,
	maxVolumeNumber = 20,
	dropVolumeOnFull = True)
 ```
  
  
then start the server

  ```python	
d.start()
  ```

and send some data

  ```python
d.sendData(data, time = 0, channel = 1, color ="1.0 0.4 0.2 1.0") 
  ```


###Example 

  ```python
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
  ```
  
## Acknowledgements
For opening tif and czi files pyclearvolume uses the excellent modules "tifffile" and "czifile" from [Christoph Gohlke](http://www.lfd.uci.edu/~gohlke/).
