"""
This modules exports the format in BIN file
"""

import os
from pathlib import Path
import datetime
from array import array
import struct
from typing import List
from typing import Any
from . import constant


class CFWBINARY:
    magic = [b'C', b'F', b'W', b'B']    # 4 characters "CFWB"
    Version = constant.CFWB_VERSION     # 32-bit int
    secsPerTick = 0.0                   # double 8-byte
    Year = 0                            # 32-bit int
    Month = 0                           # 32-bit int
    Day = 0                             # 32-bit int
    Hour = 0                            # 32-bit int
    Minute = 0                          # 32-bit int
    Second = 0.0                        # double 8-byte
    trigger = 0.0                       # double 8-byte
    NChannels = 0                       # 32-bit int
    SamplesPerChannel = 0               # 32-bit int
    TimeChannel = 0                     # 32-bit int
    DataFormat = 0                      # 32-bit int

    def __init__(self, secsPerTick: float = 0.0, Year: int = 0, Month: int = 0, Day: int = 0,
                 Hour: int = 0, Minute: int = 0, Second: float = 0.0, trigger: float = 0.0,
                 NChannels: int = 0, SamplesPerChannel: int = 0, TimeChannel: int = 0,
                 DataFormat: int = constant.FORMAT_SHORT):
        self.secsPerTick = secsPerTick
        self.Year = Year
        self.Month = Month
        self.Day = Day
        self.Hour = Hour
        self.Minute = Minute
        self.Second = Second
        self.trigger = trigger
        self.NChannels = NChannels
        self.SamplesPerChannel = SamplesPerChannel
        self.TimeChannel = TimeChannel
        self.DataFormat = DataFormat

    def setValue(self, secsPerTick: float = 0.0, Year: int = 0, Month: int = 0, Day: int = 0,
                 Hour: int = 0, Minute: int = 0, Second: float = 0.0, trigger: float = 0.0,
                 NChannels: int = 0, SamplesPerChannel: int = 0, TimeChannel: int = 0,
                 DataFormat: int = constant.FORMAT_SHORT):
        self.secsPerTick = secsPerTick
        self.Year = Year
        self.Month = Month
        self.Day = Day
        self.Hour = Hour
        self.Minute = Minute
        self.Second = Second
        self.trigger = trigger
        self.NChannels = NChannels
        self.SamplesPerChannel = SamplesPerChannel
        self.TimeChannel = TimeChannel
        self.DataFormat = DataFormat


class CFWBCHANNEL:
    Title = ""              # 32 characters long
    Units = ""              # 32 characters long
    scale = 0.0             # double 8-byte
    offset = 0.0            # double 8-byte
    RangeHigh = 0.0         # double 8-byte
    RangeLow = 0.0          # double 8-byte

    def __init__(self, Title: str = "", Units: str = "", scale: float = 0.0, offset: offset = 0.0,
                 RangeHigh: float = 0.0, RangeLow: float = 0.0):
        self.Title = Title
        self.Units = Units
        self.scale = scale
        self.offset = offset
        self.RangeHigh = RangeHigh
        self.RangeLow = RangeLow

    def setValue(self, Title: str = "", Units: str = "", scale: float = 0.0, offset: offset = 0.0,
                 RangeHigh: float = 0.0, RangeLow: float = 0.0):
        self.Title = Title
        self.Units = Units
        self.scale = scale
        self.offset = offset
        self.RangeHigh = RangeHigh
        self.RangeLow = RangeLow


class BinFileError(BaseException):
    def __init__(self, message):
        self.message = message


class BinFile:
    f = None
    filename = ""
    header = None
    channels = []

    def __init__(self, filename: str, mode: str):
        self.filename = filename
        self.mode = mode
        self.header = None
        self.channels = []

    def open(self):
        if self.mode == "r":
            try:
                self.f = open(self.filename, "rb")
            except:
                self.f = None
        elif self.mode == "r+":
            try:
                self.f = open(self.filename, "rb+")
            except:
                self.f = None
        elif self.mode == "w":
            try:
                outfile = Path(self.filename)
                if not outfile.exists():
                    self.f = open(self.filename, "wb")
                else:
                    raise
            except:
                self.f = None
                raise BinFileError("Cannot open file!")

    def setHeader(self, header: CFWBINARY):
        self.header = header

    def addChannel(self, channelDef: CFWBCHANNEL):
        self.channels.append(channelDef)

    def readHeader(self):
        intsize = struct.calcsize("i")
        doublesize = struct.calcsize("d")
        self.header = CFWBINARY()
        self.header.magic[0], self.header.magic[1], self.header.magic[2], self.header.magic[3] = struct.unpack("cccc", self.f.read(4))
        self.header.Version = struct.unpack("i", self.f.read(intsize))[0]
        self.header.secsPerTick = struct.unpack("d", self.f.read(doublesize))[0]
        self.header.Year, self.header.Month, self.header.Day, self.header.Hour, self.header.Minute = struct.unpack("iiiii", self.f.read(intsize * 5))
        self.header.Second, self.header.trigger = struct.unpack("dd", self.f.read(doublesize * 2))
        self.header.NChannels, self.header.SamplesPerChannel, self.header.TimeChannel, self.header.DataFormat = struct.unpack("iiii", self.f.read(intsize * 4))
        self.channels = []
        for i in range(self.header.NChannels):
            buf = self.f.read(32)
            label = buf.decode("ASCII").rstrip('\0')
            buf = self.f.read(32)
            uom = buf.decode("ASCII").rstrip('\0')
            scale, offset, rangeHigh, rangeLow = struct.unpack("dddd", self.f.read(doublesize * 4))
            channel = CFWBCHANNEL(label, uom, scale, offset, rangeHigh, rangeLow)
            self.channels.append(channel)

    def writeHeader(self):
        # set to beginning of file
        self.f.seek(0, 0)
        self.f.write(struct.pack("cccc", self.header.magic[0], self.header.magic[1], self.header.magic[2], self.header.magic[3]))
        self.f.write(struct.pack("i", self.header.Version))
        self.f.write(struct.pack("d", self.header.secsPerTick))
        self.f.write(struct.pack("i", self.header.Year))
        self.f.write(struct.pack("i", self.header.Month))
        self.f.write(struct.pack("i", self.header.Day))
        self.f.write(struct.pack("i", self.header.Hour))
        self.f.write(struct.pack("i", self.header.Minute))
        self.f.write(struct.pack("d", self.header.Second))
        self.f.write(struct.pack("d", self.header.trigger))
        self.f.write(struct.pack("i", self.header.NChannels))
        self.f.write(struct.pack("i", self.header.SamplesPerChannel))
        self.f.write(struct.pack("i", self.header.TimeChannel))
        self.f.write(struct.pack("i", self.header.DataFormat))
        # Write out 'NChannels' of channel headers
        if (self.channels is not None) and (len(self.channels) > 0):
            for i in range(len(self.channels)):
                channel = self.channels[i]
                length = len(channel.Title)
                if length > 32:
                    length = 32
                for j in range(length):
                    self.f.write(struct.pack("c", channel.Title[j].encode('ASCII')))
                length = 32 - len(channel.Title)
                if length < 0:
                    length = 0
                for j in range(length):
                    self.f.write(struct.pack("c", b'\0'))
                length = len(channel.Units)
                if length > 32:
                    length = 32
                for j in range(len(channel.Units)):
                    self.f.write(struct.pack("c", channel.Units[j].encode('ASCII')))
                length = 32 - len(channel.Units)
                if length < 0:
                    length = 0
                for j in range(length):
                    self.f.write(struct.pack("c", b'\0'))
                self.f.write(struct.pack("d", channel.scale))
                self.f.write(struct.pack("d", channel.offset))
                self.f.write(struct.pack("d", channel.RangeHigh))
                self.f.write(struct.pack("d", channel.RangeLow))

    def writeChannelData(self, chanData: List[List[Any]], fs: int = 0, gapInSecs: int = 0):
        # 2 means the end of file
        self.f.seek(0, 2)
        numSamplesWritten = 0
        numChannels = len(chanData)
        if gapInSecs > 0:
            numSamples = gapInSecs * fs
            numSamplesWritten += numSamples
            for j in range(numSamples):
                for i in range(numChannels):
                    if self.header.DataFormat == constant.FORMAT_SHORT:
                        d = -32767
                        self.f.write(struct.pack("h", d))
                    elif self.header.DataFormat == constant.FORMAT_DOUBLE:
                        d = -2147483647
                        self.f.write(struct.pack("d", d))
                    elif self.header.DataFormat == constant.FORMAT_FLOAT:
                        d = -sys.float_info.max
                        self.f.write(struct.pack("f", d))
        overlappedSamples = (-1 * gapInSecs * fs) if gapInSecs < 0 else 0
        numSamplesWritten += max(len(chanData[0]) - overlappedSamples, 0)
        for j in range(len(chanData[0])):
            if j < overlappedSamples:
                continue
            for i in range(len(chanData)):
                # bug fix, prevent idx out of range
                out_of_range = j > (len(chanData[i]) - 1)
                if self.header.DataFormat == constant.FORMAT_SHORT:
                    d = chanData[i][j] if not out_of_range else -32767
                    self.f.write(struct.pack("h", d))
                elif self.header.DataFormat == constant.FORMAT_DOUBLE:
                    d = chanData[i][j] if not out_of_range else -2147483647
                    self.f.write(struct.pack("d", d))
                elif self.header.DataFormat == constant.FORMAT_FLOAT:
                    d = chanData[i][j] if not out_of_range else -sys.float_info.max
                    self.f.write(struct.pack("f", d))
                else:
                    # raise exception
                    raise BinFileError("Unsupported array type!")
        return numSamplesWritten

    def updateSamplesPerChannel(self, numSamples: int, writeToFile: bool):
        self.header.SamplesPerChannel = numSamples
        if writeToFile:
            if self.mode == "w" or self.mode == "r+":
                self.f.seek(constant.N_SAMPLE_POSITION)
                self.f.write(struct.pack("i", numSamples))
                self.f.flush()

    def closeFile(self):
        # print("CloseFile")
        if self.f is not None:
            self.f.flush()
            self.f.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, type, value, traceback):
        self.closeFile()