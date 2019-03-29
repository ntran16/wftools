import numpy as np
# to fix error in pyinstaller, we need to import additional types for numpy
import numpy.core._dtype_ctypes
from array import array
from typing import List


# use numpy's interp (linear interpolation)
# or scipy's interp1d to have more options for interpolation
# But scipy has to specify option to handle x-range out of bound (extrapolation)
def fixsamplinglist(arr: List[float], samplesPerSec: float, targetSamplesPerSec: float):
    x = np.array(list(range(0, len(arr))))
    y = np.array(arr)
    step = samplesPerSec / targetSamplesPerSec
    new_x = []
    for u in np.arange(0, len(arr), step):
        new_x.append(u)
    '''
    fill_value = (y[0], y[len(y) - 1])
    f = interpolate.interp1d(x, y, bounds_error=False, fill_value=fill_value)
    new_y = f(new_x)
    '''
    new_y = np.interp(new_x, x, y)
    return new_y.tolist()


def fixsamplingarr(arr: array, samplesPerSec: float, targetSamplesPerSec: float):
    x = np.array(list(range(0, len(arr))))
    y = np.array(arr)
    step = samplesPerSec / targetSamplesPerSec
    new_x = []
    for u in np.arange(0, len(arr), step):
        new_x.append(u)
    '''
    fill_value = (y[0], y[len(y) - 1])
    f = interpolate.interp1d(x, y, bounds_error=False, fill_value=fill_value)
    new_y = f(new_x)
    '''
    new_y = np.interp(new_x, x, y)
    return array('h', new_y.astype(int).tolist())
