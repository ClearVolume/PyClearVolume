"""
packages data into the raw format the clearvolume client expects

author: Martin Weigert
email: mweigert@mpi-cbg.de
"""

from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import six
from six.moves import zip

DEFAULT_METADATA = {
    "index": 0,
    "time": 0,
    "channel": 0,
    "channelname": "python source",
    "viewmatrix": "1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.",
    "dim": 3,
    "color": (1., 1., 1., 1.),
    "type": "UnsignedShort",
    "bytespervoxel": 2,
    "elementsize": 1,
    "voxelwidth": 1,
    "voxelheight": 1,
    "voxeldepth": 1,
    "realunit": 1
}

_SUPPORTED_TYPES = {np.uint8: "UnsignedByte",
                    np.uint16: "UnsignedShort"}


def _serialize_data(data, meta=DEFAULT_METADATA):
    """returns serialized version of data for clearvolume data viewer"""

    if not isinstance(data, np.ndarray):
        raise TypeError("data should be a numpy array (but is %s)" % type(data))

    if not data.dtype.type in _SUPPORTED_TYPES:
        raise ValueError("data type should be in (%s) (but is %s)" % (list(_SUPPORTED_TYPES.keys()), data.dtype))

    LenInt64 = len(np.int64(1).tostring())

    Ns = data.shape

    metaData = DEFAULT_METADATA.copy()

    # prepare header....

    metaData["type"] = _SUPPORTED_TYPES[data.dtype.type]

    for attrName, N in zip(["width", "height", "depth"], Ns[::-1]):
        metaData[attrName] = meta.get(attrName, N)

    for key, val in six.iteritems(meta):
        if key not in metaData:
            raise KeyError(" '%s' (= %s) as is an unknown property!" % (key, val))
        else:
            metaData[key] = val

    print(metaData)

    keyValPairs = [str(key) + ":" + str(val) for key, val in six.iteritems(metaData)]
    headerStr = ",".join(keyValPairs)
    headerStr = "[" + headerStr + "]"

    # headerStr = str(metaData).replace("{","[").replace("}","]").replace("'",'')#.replace(" ",'')


    headerLength = len(headerStr)

    dataStr = data.tostring()
    dataLength = len(dataStr)

    neededBufferLength = 3 * LenInt64 + headerLength + dataLength

    return "%s%s%s%s%s" % (np.int64(neededBufferLength).tostring(), np.int64(headerLength).tostring(), headerStr,
                           np.int64(dataLength).tostring(), dataStr)


if __name__ == '__main__':
    Ns = [1, 2, 3]

    d = (123 * np.linspace(0, 200, np.prod(Ns))).reshape(Ns).astype(np.uint8)

    # dStr = _serialize_data(d,{"width": 5.,"color":"1. .5 .2 1."})

    dStr = _serialize_data(d, {"width": "5", "color": "1. .5 .2 1."})

    # print dStr
