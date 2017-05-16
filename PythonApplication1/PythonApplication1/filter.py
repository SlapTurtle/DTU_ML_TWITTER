import re
from os import walk
import dataGathering as dg
import preprocessing as prep
import PythonApplication1 as main

TAGS = set()
DP = ""

def filterfolder():
    print("Filtering all files")
    path = main.directorySkip() + main.PRE_PATH
    _,_, filenames = next(walk(path))

    for file in filenames:
        filterfile(file[:-6])


def filterfile(file):
    global TAGS, DP
    TAGS = getTags()
    print("Filtering file " + file)
    DP = main.getDataPath(main.FILTER_PATH + file + "_f")
    clearfile(DP)
    file = main.getDataPath(main.PRE_PATH + file + "_p")

    with open(file, "r", encoding='utf8') as f:
        for line in f:
            s = filter(line)
            if (len(s) != 0):
                with open(DP, "a") as dp:
                    dp.write(s)


def filter(s):
    list = re.split("\W+|_", s)
    for word in list:
        if (word in TAGS):
            return s
    return ""


def getTags():
    path = main.getDataPath(main.FILE_tag + "_f")
    tags = set()
    with open(path, "r") as file:
        for line in file:
            tags.add(line[:-1])
    return tags


def clearfile(file):
    with open(file, "w") as f:
        f.write("")