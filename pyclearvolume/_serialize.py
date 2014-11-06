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
	"dim": 3,
	"type": "Byte",
	"bytespervoxel":1,
	"elementsize": 1,
	"widthreal": 1,
	"heightreal": 1,
	"depthreal": 1,
	"realunit":1
    }



def _serialize_data(data, meta = DEFAULT_METADATA ):
    """returns serialized version of data for clearvolume data viewer"""

    LenInt64 = len(np.int64(1).tostring())

    Ns = data.shape

    metaData = DEFAULT_METADATA.copy()
    #prepare header....
    for attrName,N in zip(["widthvoxels","heightvoxels","depthvoxels"],Ns[::-1]):
        metaData[attrName] = meta.get(attrName,N)

    for key, val in meta.iteritems():
        if not metaData.has_key(key):
            raise KeyError(" '%s' (= %s) as is an unknown property!"%(key, val))
        else:
            metaData[key] = val


    headerStr = str(metaData).replace("{","[").replace("}","]").replace("'",'').replace(" ",'')

    
    headerLength = len(headerStr)

    dataStr = data.tostring()
    dataLength = len(dataStr)

    neededBufferLength = 3*LenInt64 + headerLength + dataLength

    return "%s%s%s%s%s"%(np.int64(neededBufferLength).tostring(),np.int64(headerLength).tostring(),headerStr,np.int64(dataLength).tostring(),dataStr)



if __name__ == '__main__':


    Ns = [11,12,13]

    d = (123*np.linspace(0,200,np.prod(Ns))).reshape(Ns).astype(np.uint8)


    dStr = _serialize_data(d,{"widthreal": 5.})
