"""
This modules provides XML conversion to Bin file
"""
import datetime
from datetime import datetime
from dateutil import parser
from typing import List
from typing import Any

WAVE_FORMAT_DOUBLE = 1
WAVE_FORMAT_FLOAT = 2
WAVE_FORMAT_SHORT = 3


class WaveHeader:
    samplesPerSec = 0
    startDt = datetime.min
    numChannels = 0
    dataFormat = WAVE_FORMAT_DOUBLE

    def __init__(self, samplesPerSec: int = 0, startDt: Any = None,
                 numChannels: int = 0, dataFormat: int = WAVE_FORMAT_DOUBLE):
        self.samplesPerSec = samplesPerSec
        self.startDt = datetime.min
        startDt = parser.parse(startDt) if isinstance(startDt, str) else startDt
        self.startDt = startDt if (startDt is not None) else datetime.min
        self.numChannels = numChannels
        self.dataFormat = dataFormat


class WaveChannel:
    label = ""
    uom = ""
    scale = 0.0
    offset = 0.0
    rangeHigh = 0.0
    rangeLow = 0.0

    def __init__(self, label: str = "", uom: str = "", scale: float = 0.0, offset: float = 0.0,
                 rangeHigh: float = 0.0, rangeLow: float = 0.0):
        self.label = label
        self.uom = uom
        self.scale = scale
        self.offset = offset
        self.rangeHigh = rangeHigh
        self.rangeLow = rangeLow


class XmlConverterError(BaseException):
    def __init__(self, message):
        self.message = message
