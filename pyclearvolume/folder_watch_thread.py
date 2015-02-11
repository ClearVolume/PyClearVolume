"""

a simple utility that watches a folder for new image files and
returns the data

"""


import os
from Queue import Queue
from threading import Thread

from sortedcontainers import SortedList

from pyclearvolume.image_file_reader import ImageFolderReader,  ImageFileReader

import time

class WatchThread(Thread):
    """
    """

    def __init__(self,dirName, wildcard="*"):
        super(WatchThread,self).__init__()
        self.folderReader = ImageFolderReader(dirName,wildcard)
        self.fileQueue = Queue()
        self.inspected = set()
        self.add_list_to_queue(self.folderReader._update_files())
        self.setDaemon(True)
        
    def add_list_to_queue(self,fList):
        for fName in fList:
            print "adding file: ",fName
            self.fileQueue.put(fName)
            self.inspected.add(fName)
            

    def run(self):
        while True:
            allFiles = self.folderReader._update_files()
            newFiles = sorted(set(allFiles).difference(self.inspected))
            self.add_list_to_queue(newFiles)
            time.sleep(.001)

    def empty(self):
        return self.fileQueue.empty()

    def get(self):
        fName = self.fileQueue.get()
        print "getting data from ", fName
        data, meta =  ImageFileReader.load_file(fName)
        print "shape: ", data.shape
        return data, meta
            
            
        

    
if __name__ == "__main__":

    a = WatchThread("/Users/mweigert/python/bioformats_test/data")


    a.start()

    while True:
        if not a.empty():
            print  a.get().shape
        time.sleep(.1)

    
