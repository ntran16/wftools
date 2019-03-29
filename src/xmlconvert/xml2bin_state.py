import os
import datetime
from myutil import parsetime


class Xml2BinState:
    lastBinFilename = ""
    numVitalsignTypes = 0
    vitalsignName = []
    lastVitalFilename = []
    startVitalTm = []
    xmlStartTm = None
    xmlEndTm = None
    timestampTm = ""

    def __init__(self):
        self.lastBinFilename = ""
        self.numVitalsignTypes = 0
        self.vitalsignName = []
        self.lastVitalFilename = []
        self.startVitalTm = []
        self.xmlStartTm = None
        self.xmlEndTm = None
        self.timestampTm = None

    def freeXmlBinState(self):
        self.lastBinFilename = ""
        self.numVitalsignTypes = 0
        self.vitalsignName = []
        self.lastVitalFilename = []
        self.startVitalTm = []
        self.xmlStartTm = None
        self.xmlEndTm = None
        self.timestampTm = None

    def setLastBinFilename(self, fn: str):
        self.lastBinFilename = fn

    def setTimestampTm(self, timestamp: object):
        if isinstance(timestamp, str):
            self.timestampTm = parsetime(timestamp)
        elif isinstance(timestamp, datetime.datetime):
            self.timestampTm = timestamp

    def setXmlStartEndTm(self, startTimeStr: str, endTimeStr: str):
        self.xmlStartTm = parsetime(startTimeStr)
        self.xmlEndTm = parsetime(endTimeStr)
