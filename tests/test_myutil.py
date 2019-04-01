import os
import sys
from myutil import parsetime


def test_parsetime():
    timestr = "11/19/2018 23:50:39"
    dt = parsetime(timestr)
    result = dt.strftime("%m/%d/%Y %H:%M:%S")
    assert(timestr == result)
