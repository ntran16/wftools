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
