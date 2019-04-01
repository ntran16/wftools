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
from typing import Dict


# tagDict should be something like:
# { "id1": "some_str", "id2": "some_str"... "id5": "some_str", "starttime": "some_str", "exetime": "some_str"}
# fnpattern should be something like:
# "{id1}_{starttime}_{exetime}_{id2}_{id3}"
def getOutputFilename(outputDir: str, fnpattern: str, tagsDict: Dict, fileext: str):
    filename = fnpattern.format(**tagsDict)
    i = 1
    buf = "{0}{1}{2}.{3}".format(outputDir, os.path.sep, filename, fileext)
    while (os.path.exists(buf)):
        buf = "{0}{1}{2}_{3}.{4}".format(outputDir, os.path.sep, filename, i, fileext)
        i += 1
    return buf
