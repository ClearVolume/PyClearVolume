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
    def _list_supported_files_with_timestamp(cls,dirName, wildcard = "*"):
        files = [(f, os.path.getsize(f))
                 for f in glob.glob(os.path.join(dirName,wildcard))
                 if cls.is_supported(f)]


class ImageFolderReader(object):
    def __init__(self,dirName = None, wildcard = "*"):
        if dirName is None:
            self.dirName = None
        else:
            self.load_dir(dirName, wildcard)

    def load_dir(self,dirName, wildcard):
        if os.path.isdir(dirName):
            self.dirName = dirName
            self.wildcard = wildcard
            self._update_files()
        else:
            raise IOError("Directory not found: %s"%dirName)

    def _update_files(self):
        self.files = [fName for fName in
                      glob.glob(os.path.join(self.dirName,self.wildcard))
                      if ImageFileReader.is_supported(fName)]
        
        return self.files

    def __iter__(self):
        for fName in self.files:
            data, meta = ImageFileReader.load_file(fName)
            yield data, meta


            
if __name__ == "__main__":

    # fName = "data/retina.czi"
    
    a = ImageFolderReader("/Users/mweigert/Tmp/CVTmp/")


    for fName, (data, meta) in zip(a.files, a):
        print fName, data.shape
