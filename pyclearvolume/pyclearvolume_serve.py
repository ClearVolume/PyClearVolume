#!/usr/local/bin/python

import numpy as np
import time
import argparse 
import sys
import os

from pyclearvolume.folder_watch_thread import WatchThread
from pyclearvolume.image_file_reader import ImageFileReader

import pyclearvolume


def _extract_3d(data):
    """ in case data has more then 3 dims, extract the 3 biggest ones
    e.g. for czi files
    """
    return np.squeeze(data)


def _prepare_data(data):
    """ensure data is a nice uint16 array"""
    if data.ndim < 3:
        raise ValueError("data has invalid dimensions %s"%(data.shape,))
    if data.ndim > 3:
        data = _extract_3d(data)
    
    data = data.astype(np.uint16)
    data = 255.*(data-np.amin(data))/(np.amax(data)-np.amin(data))
    return data.astype(np.uint8)
    


def _watch_folder(dirName, addr, port, dtime,**kwargs):
    d = pyclearvolume.DataServer(maxVolumeNumber=20)

    d.start()

    try:
        watchThread = WatchThread(dirName, deltaTime = dtime)
    except Exception as e:
        sys.exit(str(e))
        
    watchThread.start()

    t = 0
    while True:
        if not watchThread.empty():
            print "connected to %s %s"%(d.client_address())
            try:
                data, meta = watchThread.get()
                print "getting:  ", data.shape
                data = _prepare_data(data)
                args = {}
                args["index"] = t
                args.update(kwargs)
                print "sending data of shape %s"%(data.shape,)
                d.sendData(data,**args)
                d.serveUntilEmpty()
                t += 1
            except  Exception as e:
                print e

        time.sleep(1.)

    d.stop()

    
    
def _send_files(fNames, addr, port, **kwargs):
    files = list(fNames)
    d = pyclearvolume.DataServer(maxVolumeNumber=20)

    d.start()

    t = 0
    print files
    for fName in files:
        print fName
        try:
            data, meta = ImageFileReader.load_file(fName)
            data = _prepare_data(data)

            args = {}
            args["index"] = t
            args.update(kwargs)

            print "sending data of shape %s"%(data.shape,)
            d.sendData(data,**args)
            d.serveUntilEmpty()
            time.sleep(.1)
            t += 1
        except Exception as e:
            print e
       
    d.stop()

def _listdir_full(dirName):
    return [os.path.join(dirName, fName) for fName in os.listdir(dirName)]

def _iter_file_folder_list(fNames):
    for fName in fNames:
        if os.path.isdir(fName):
            for f in _iter_file_folder_list(_listdir_full(fName)):
                yield f
        else:
            yield fName
            
                    
                
class MyFormatter(argparse.ArgumentDefaultsHelpFormatter):

    def _fill_text(self, text, width, indent):
        
        return ''.join([indent + line for line in text.splitlines(True)])

    
def main():
    parser = argparse.ArgumentParser(formatter_class=MyFormatter,
        description="""
serves 3d image files or folder to a clearvolume client
    
pyclearvolume_serve  myfile.tif\n
pyclearvolume_serve -u 1. 1. 2. -a remote.domain.com -p 9140 myfile.tif 

        """)

    parser.add_argument("-a","--address",dest="address",
                        help = """address to bind to""",
                        type=str,default = "", required = False)

    parser.add_argument("-p","--port",dest="port",
                        help = """port to bind to""",
                        type=int,default = 9140, required = False)

    parser.add_argument("-w","--watch",dest="watch",
                        help = """watch folder""",
                        action="store_true")

    parser.add_argument("-t","--time",dest="dtime",
                        help = """time in secs in watch mode to
                        wait for file not having changed""",
                        type=float,default = 1., required = False)

    parser.add_argument("-u","--units",dest="units",
                        help = """relative units of voxels e.g. -u 1. 1. 2.""",
                        type=float,nargs= 3 ,default = [1.,1.,1.], required=False)
    
    parser.add_argument("-c","--color",dest="color",
                        help = """color rgb in 0..1""",
                        type=float,nargs= 3 ,default = [1.,1.,1.], required=False)
  
    parser.add_argument("files", help="image files or folder to send/watch (currently supported: %s"%(str(ImageFileReader._supported.keys())), nargs="+") 





    if len(sys.argv)==1:
        parser.print_help()
        sys.exit()

    args = parser.parse_args()

    for k,v in vars(args).iteritems():
        print k,v

    kwargs = dict()

    kwargs["voxelwidth"] = args.units[0]
    kwargs["voxelheight"] = args.units[1]
    kwargs["voxeldepth"] = args.units[2]
    kwargs["color"] = "%s %s %s 1."%tuple(args.color)

        
    if args.watch:
        dirName = args.files[0]
        if not os.path.isdir(dirName):
            raise ValueError("not a valid directory: %s"%dirName)
        else:
            _watch_folder(dirName,args.address,args.port,args.dtime,**kwargs)

    else:
        fNames = [f for f in _iter_file_folder_list(args.files)]
        print fNames
        _send_files(fNames,args.address,args.port,**kwargs)

    
if __name__ == "__main__":
    main()
