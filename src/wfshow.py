import os
import sys
import re
import yaml
import argparse
from datetime import datetime
from pathlib import Path
from array import array
from binfilepy import BinFile
import matplotlib.pyplot as plt
import numpy as np
# to fix error in pyinstaller, we need to import additional types for numpy
import numpy.core._dtype_ctypes
from typing import Any
from typing import List

g_version = "0.1"
g_exename = "wfshow"
default_config_fn = "{0}_config.yaml".format(g_exename)


def getArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="Input File", required=True)
    parser.add_argument("-s", "--start", help="Offset from start of file", required=True)
    parser.add_argument("-n", "--length", help="Length of samples", required=True)
    parser.add_argument("--size", help="Size of the graph in pixels (e.g. 1024x768)")
    parser.add_argument("--num_samples", help="Use number of samples as unit for offset and length (instead of # of seconds)", action="store_true")
    parser.add_argument("--show_header_only", help="Show header info only without plotting graphs", action="store_true")
    return parser.parse_args()


def findMinMaxStep(arr: np.ndarray):
    # Try to Auto-fit the curve in the min/max range
    min_thres = -1000
    max_thres = 1000
    n = len(arr)
    _min = sys.float_info.max
    _max = -sys.float_info.max
    for i in range(0, n):
        if (arr[i] < _min) and (arr[i] >= min_thres):
            _min = arr[i]
        if (arr[i] > _max) and (arr[i] <= max_thres):
            _max = arr[i]
    if _min == sys.float_info.max:  # never assigned
        _min = min_thres
    if _min < min_thres:
        _min = min_thres
    if _max == -sys.float_info.max:  # never assigned
        _max = max_thres
    if _max > max_thres:
        _max = max_thres
    _min = round(_min, 2)
    _max = round(_max, 2)
    if (_min == _max):
        _min -= 1
        _max += 1
    _step = round((_max - _min) / 5, 2)
    _max += _step
    _min -= _step
    return _min, _max, _step


def plotChannels(fp: str, f: BinFile, data: List[array], width: int, height: int):
    filename = Path(fp).name
    numChannels = len(data)
    numSamples = len(data[0])
    t = np.arange(0, numSamples, 1)
    s = []
    fig = None
    axs = None
    for d in data:
        s.append(np.array(d))
    if (width <= 0) or (height <= 0):
        fig, axs = plt.subplots(numChannels, 1, sharex=True)
    else:
        fig, axs = plt.subplots(numChannels, 1, sharex=True, figsize=(width / 100.0, height / 100.0), dpi=100)
    # Remove horizontal space between axes
    fig.subplots_adjust(hspace=0)
    # Plot each graph, and manually set the y tick values
    for i in range(0, numChannels):
        axs[i].plot(t, s[i])
        _min, _max, _step = findMinMaxStep(s[i])
        axs[i].set_yticks(np.arange(_min, _max, _step))
        axs[i].set_ylim(_min, _max)
        axs[i].set_ylabel(f.channels[i].Title)
    fig.suptitle(filename)
    plt.show()
    return


def printHeaderInfo(f: BinFile):
    print("Binary file info:")
    dt = datetime.strptime("{0}/{1}/{2} {3}:{4}:{5:.0f}".format(f.header.Year, f.header.Month, f.header.Day, f.header.Hour, f.header.Minute, f.header.Second), "%Y/%m/%d %H:%M:%S")
    print("Start Date/Time: {0}".format(dt.strftime("%Y/%m/%d %H:%M:%S")))
    print("Secs Per Tick: {0:.6f}".format(f.header.secsPerTick))
    print("Samples Per Sec: {0:.3f}".format(1.0 / f.header.secsPerTick))
    print("Data Format: {0}".format(f.header.DataFormat))
    print("#Samples: {0}".format(f.header.SamplesPerChannel))
    print("#Channels: {0}".format(f.header.NChannels))
    for c in f.channels:
        print("  Channel: {0}".format(c.Title))
        print("    - Uom: {0}".format(c.Units))
        print("    - Scale: {0}".format(c.scale))
        print("    - Offset: {0}".format(c.offset))
        print("    - RangeLow: {0}".format(c.RangeLow))
        print("    - RangeHigh: {0}".format(c.RangeHigh))


def runApp(fn, offset, length, width, height, useNumSamples, showHeaderOnly):
    with BinFile(fn, "r") as f:
        f.readHeader()
        printHeaderInfo(f)
        if not showHeaderOnly:
            data = f.readChannelData(offset, length, useSecForOffset=not useNumSamples, useSecForLength=not useNumSamples)
            if (data is not None) and (len(data) > 0):
                numSamples = len(data[0])
                if numSamples > 0:
                    plotChannels(fn, f, data, width, height)
    return

print("{0} v{1} - Copyright(c) HuLab@UCSF 2019".format(g_exename, g_version))
args = getArgs()
width = 0
height = 0
if args.size is not None:
    s = args.size.split("x")
    if len(s) == 2:
        width = int(s[0])
        height = int(s[1])
    else:
        print("--size argument must be in the form of 'WxH', like 680x480 !!")
        valid = False
runApp(args.file, float(args.start), float(args.length), width, height, args.num_samples, args.show_header_only)
print("done.")
