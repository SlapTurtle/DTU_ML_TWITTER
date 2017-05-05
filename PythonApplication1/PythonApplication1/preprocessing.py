import PythonApplication1 as main
import re

from string import digits
from time import time

FILE = "2017Mar17"

POSITIVES = set()
NEGATIVES = set()

# HUSK: at måske undgå split ved '-'

def parseSet(file = "SentimentAnalysisDataset"):
    clearfile("ds_pos")
    clearfile("ds_neg")
    time_start = time()
    print("Parsing set . . .")
    with open(main.getDataPath(file), "r", encoding='utf8') as f:
        k = 0
        for line in f:
            line = str(line.encode('utf-8')).replace('\n','')
            i,j = 0,0
            pos = None
            while(j<3):
                if(line[i] == ','):
                    j += 1
                    if(j == 1):
                        pos = (line[i+1] == '1')                 
                i += 1

            ds = "ds_pos_p" if pos else "ds_neg_p"
            with open(main.getDataPath(ds), "a") as fi:
                fi.write(prep(line[i:])[:-2] + "\n")
            k += 1

            if k % 1000 == 0:
                print("Finished " + str(k))
    time_end = time()
    print("Processed " + FILE + " in " + (str)(time_end - time_start)[:4] + "s")

def processMar():
    for date in range(30,32):
        process("2017Mar" + str(date))

def processApr():
    for date in range(10,15):
        process("2017Apr" + str(date))

def process(file = FILE):
    global POSITIVES, NEGATIVES

    time_start = time()
    data = open(main.getDataPath(main.RAW_PATH + file))
    clearfile(main.PRE_PATH + file)

    recent = [""] * 60
    index = 0

    POSITIVES = set(main.loadFile("positives"))
    NEGATIVES = set(main.loadFile("negatives"))

    for line in data:
        text = get_text(line)
        result = prep(text)
        spam = False
        for r in recent:
            if result == r:
                spam = True
                break
        if not spam:
            filedump(result + "\n", file)
            recent[index] = result
            if (1 + index < len(recent)):
                index = index + 1
            else:
                index = 0

    time_end = time()
    print("Processed " + file + " in " + (str)(time_end - time_start)[:4] + "s")

# get text from data string
def get_text(string):
    string = string.replace('\"', "'", 1)
    date, text = string.split("'", 1)
    return text[:-1]


# prep
def prep(string):
    tokenized = tokenize(re.sub('[\']', '', string))
    prol = alter_prolonged(tokenized)
    result = ""
    for t in prol:
        result = result + t + " "
    return result[:-1]

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
    res = list.copy()
    for v in range(len(list)):
        i = 0
        j = -1
        w = list[v]
        while(i + 2 < len(w)):
            if (w[i] == w[i+1] and w[i+1] == w[i+2]):
                w = w[:i] + w[(i+1):]
                j = i
            else:
                i+= 1
        if (not (w in POSITIVES or w in NEGATIVES)) and j != -1:
            w = w[:j] + w[(j+1):]
        res[v] = w
    return res


# clear file before writing
def clearfile(file = FILE):
    dp = main.getDataPath(file)[:-4] + "_p.txt"
    with open(dp, "w") as f:
        f.write("")

# write to _p file
def filedump(s, file = FILE):
    dp = main.getDataPath(main.PRE_PATH + file)[:-4] + "_p.txt"
    with open(dp, "a") as file:
        file.write(s)