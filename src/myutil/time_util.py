"""
MIT License

Copyright (c) 2019 UCSF Hu Lab

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

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
