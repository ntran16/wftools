import os
import sys
import re
import yaml
import argparse
import datetime
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
    parser.add_argument("--use_num_samples_for_start", help="Offset interpreted as number of samples (instead of seconds)", action="store_true")
    parser.add_argument("--use_num_samples_for_length", help="Length interpreted as number of samples (instead of seconds)", action="store_true")
    return parser.parse_args()


def findMinMaxStep(arr: np.ndarray):
    # Need to improve
    # I am lazy... so just pick a small number for NaN (like gap)
    nan = -1000
    n = len(arr)
    _min = None
    _max = None
    for i in range(0, n):
        if _min == None:
            _min = arr[i]
        if _max == None:
            _max = arr[i]
        if arr[i] < _min and arr[i] > nan:
            _min = arr[i]
        if arr[i] > _max:
            _max = arr[i]
    if _min < nan:
        _min = 0
    _min = round(_min, 2) 
    _max = round(_max, 2)
    _step = round((_max - _min) / 5, 2)
    _max += _step / 2
    _min -= _step /2
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
        fig, axs = plt.subplots(numChannels, 1, sharex=True, figsize=(width/100.0, height/100.0), dpi=100)
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

def runApp(fn, offset, length, width, height, useNumSamplesForWidth, useNumSamplesForLength):
    with BinFile(fn, "r") as f:
        f.readHeader()
        data = f.readChannelData(offset, length, useNumSamplesForWidth == False, useNumSamplesForLength == False)
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
runApp(args.file, float(args.start), float(args.length), width, height, args.use_num_samples_for_start, args.use_num_samples_for_length)
print("done.")
