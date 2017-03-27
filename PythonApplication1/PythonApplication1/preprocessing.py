import re
from string import digits
from PythonApplication1 import *
from time import time

FILE = "2017Mar16"
DATA_PATH = 'Files\\'

# HUSK: at undgå split ved '-'

def process():
    time_start = time()
    data = open(getDataPath(FILE))
    clearfile()

    recent = [""] * 60
    index = 0

    for line in data:
        text = get_text(line)
        tokenized = tokenize(text)
        result = re.sub(r"[^A-Za-z ]+", '', str(tokenized))

        spam = False
        for r in recent:
            if result == r:
                spam = True
                break
        if not spam:
            filedump(result + "\n")
            recent[index] = result
            if (1 + index < len(recent)):
                index = index + 1
            else:
                index = 0

    time_end = time()
    print("Processed " + FILE + " in " + (str)(time_end - time_start)[:4] + "s")


# get text from data string
def get_text(string):
    string = string.replace('\"', "'", 1)
    date, text = string.split("'", 1)
    return text[:-1]


# cool stuff
def tokenize(string):
    list = re.split("\W+|_", string)
    tokenized = [x.lower() for x in list]
    i = 0
    while(i != len(tokenized)):
        no_digits = str.maketrans('', '', digits)
        tokenized[i] = tokenized[i].translate(no_digits)
        word = tokenized[i]
        if (word == "https" or word == "nhttps"):
            try:
                for j in range(0,4):
                    tokenized.pop(i)
            except:
                pass
        elif (len(word) < 1) or (len(word) <= 3 and word[0] == 'x') or (word == "rt"):
            tokenized.pop(i)
        else:
            i = i + 1
    return tokenized


# alteration of prolonged words
def alter_prolonged(list = []):
    return


# clear file before writing
def clearfile():
    dp = getDataPath(FILE)[:-4] + "_p.txt"
    with open(dp, "w") as file:
        file.write("")

# write to _p file
def filedump(s):
    dp = getDataPath(FILE)[:-4] + "_p.txt"
    with open(dp, "a") as file:
        file.write(s)

def getDataPath(s):
    path = directorySkip() + s +'.txt'
    return path

def directorySkip(s=DATA_PATH):
    path = os.path.dirname(os.path.abspath(__file__))
    if type(path) == str:
        i,j = len(path),0
        while (j!=2):
            i = i-1
            if path[i] == '\\':
                j = j + 1
        return path[0:i+1] + s
    return None