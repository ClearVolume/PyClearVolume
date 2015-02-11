"""
some functions to open 3d biological volume files

supported as of now:

- 3d Tif
- CZI

it uses the tifffile and czifile libraries of
Christoph Gohlke http://www.lfd.uci.edu/~gohlke/
(for copyright and license see tifffile.py)
and python-bioformats

"""


import os
import glob 

#surpress warning of tifffile....
import warnings
warnings.filterwarnings("ignore")

from pyclearvolume import czifile
from pyclearvolume import tifffile

def _load_tif_file(fName):
    with tifffile.TiffFile(fName) as imgFile:
        data = imgFile.asarray()
        meta = None
    return data ,meta

def _load_czi_file(fName):
    with czifile.CziFile(fName) as imgFile:
        data = imgFile.asarray()
        meta = None
    return data ,meta

class ImageFileReader(object):
    """the container class for reading an image"""
 
    _supported = {".tif":_load_tif_file,
                  ".tiff":_load_tif_file,
                  ".czi":_load_czi_file}
   
    def __init__(self,fName = None):
        self.data = None
        self.meta = None
        if fName is not None:
            self.data, self.meta = self.load_file(fName)

    @classmethod
    def is_supported(cls,fName):
        basename, ext = os.path.splitext(fName)
        return cls._supported.has_key(ext)

    @classmethod
    def load_func_for(cls,fName):
        basename, ext = os.path.splitext(fName)
        return cls._supported[ext]

    @classmethod
    def load_file(cls,fName):
        if not cls.is_supported(fName):
            raise ValueError("Image format of  %s not in supported formats (%s)!"
                             %(fName,cls._supported.keys()))

        return cls.load_func_for(fName)(fName)

    @classmethod
    def _list_supported_files(cls,dirName, wildcard = "*", func = None):
        """ list all supported files in directory dirName
        
        func can be a function of the filename, in which case the result is
        the list (filename, func(filename))
        """
        if hasattr(func, '__call__'):
            return [(f, func(f))
                    for f in glob.glob(os.path.join(dirName,wildcard))
                 if cls.is_supported(f)]
        else:
            return [f for f in glob.glob(os.path.join(dirName,wildcard))
                 if cls.is_supported(f)]

            

class ImageFolderReader(object):
    def __init__(self,dirName = None, wildcard = "*", func = None):
        self.dirName = dirName
        self.wildcard = wildcard
        self.func= func    

    def list_files(self):
        return ImageFileReader._list_supported_files(
            self.dirName, self.wildcard, self.func)

    def __iter__(self):
        for fName in self.list_files():
            if isinstance(fName,(list,tuple)):
                fName = fName[0]
            data, meta = ImageFileReader.load_file(fName)
            yield data, meta


            
if __name__ == "__main__":

    # fName = "data/retina.czi"
    
    a = ImageFolderReader("/Users/mweigert/Tmp/CVTmp/")

    print a.list_files()
    for data, meta in a:
        print data.shape,meta
