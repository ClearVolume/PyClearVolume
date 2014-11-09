"""
packages data into the raw format the clearvolume client expects

author: Martin Weigert
email: mweigert@mpi-cbg.de
"""

import numpy as np


DEFAULT_METADATA = {
    "index":0,
    "time": 0,
	"channel": 0,
    "channelname": "python source",
    "color": "1. 1. 1. 1.",
    "viewmatrix": "1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.",
	"dim": 3,
	"type": "Byte",
	"bytespervoxel":1,
	"elementsize": 1,
	"voxelwidth": 1,
	"voxelheight": 1,
	"voxeldepth": 1,
	"realunit":1
    }



def _serialize_data(data, meta = DEFAULT_METADATA ):
    """returns serialized version of data for clearvolume data viewer"""

    LenInt64 = len(np.int64(1).tostring())

    Ns = data.shape

    metaData = DEFAULT_METADATA.copy()
    #prepare header....
    for attrName,N in zip(["width","height","depth"],Ns[::-1]):
        metaData[attrName] = meta.get(attrName,N)

    for key, val in meta.iteritems():
        if not metaData.has_key(key):
            raise KeyError(" '%s' (= %s) as is an unknown property!"%(key, val))
        else:
            metaData[key] = val


    keyValPairs = [str(key)+":"+str(val) for key, val in metaData.iteritems()]
    headerStr = ",".join(keyValPairs)
    headerStr = "["+headerStr+"]"
    
    # headerStr = str(metaData).replace("{","[").replace("}","]").replace("'",'')#.replace(" ",'')


    headerLength = len(headerStr)

    dataStr = data.tostring()
    dataLength = len(dataStr)

    neededBufferLength = 3*LenInt64 + headerLength + dataLength

    return "%s%s%s%s%s"%(np.int64(neededBufferLength).tostring(),np.int64(headerLength).tostring(),headerStr,np.int64(dataLength).tostring(),dataStr)



if __name__ == '__main__':


    Ns = [1,2,3]

    d = (123*np.linspace(0,200,np.prod(Ns))).reshape(Ns).astype(np.uint8)


    # dStr = _serialize_data(d,{"width": 5.,"color":"1. .5 .2 1."})

    dStr = _serialize_data(d,{"width": "5","color":"1. .5 .2 1."})

    # print dStr
