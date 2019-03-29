import os
from datetime import datetime


def dtFormat(dt: datetime):
    return ((str(dt)).split('.')[0]).split(' ')[0] + ' ' + ((str(dt)).split('.')[0]).split(' ')[1]


def dtTimestampFormat(dt: datetime, fmt: str = None):
    if (fmt is not None) and (len(fmt) > 0):
        return dt.strftime(fmt)
    return dt.strftime("%Y%m%d%H%M%S")


def elapsedFormat(seconds: float, totalSecondsOnly: bool = False):
    if totalSecondsOnly:
        return "{0:0.2f} seconds".format(seconds)
    else:
        d = divmod(seconds, 86400)  # days
        h = divmod(d[1], 3600)  # hours
        m = divmod(h[1], 60)  # minutes
        s = m[1]  # seconds
        return "{0} days, {1} hours, {2} minutes, {3:0.2f} seconds".format(int(d[0]), int(h[0]), int(m[0]), s)
    # end-if


def parsetime(s: str):
    t = None
    try:
        t = datetime.strptime(s, '%m/%d/%Y %I:%M:%S %p')
    except:
        t = None
    if (t is None):
        try:
            t = datetime.strptime(s, '%m/%d/%y %I:%M:%S %p')
        except:
            t = None
    if (t is None):
        try:
            t = datetime.strptime(s, '%Y-%m-%d %I:%M:%S %p')
        except:
            t = None
    if (t is None):
        try:
            t = datetime.strptime(s, '%m/%d/%Y %H:%M:%S')
        except:
            t = None
    if (t is None):
        try:
            t = datetime.strptime(s, '%m/%d/%y %H:%M:%S')
        except:
            t = None
    if (t is None):
        try:
            t = datetime.strptime(s, '%Y-%m-%d %H:%M:%S')
        except:
            t = None
    return t
