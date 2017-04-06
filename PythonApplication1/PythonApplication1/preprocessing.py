import re
from string import digits
from PythonApplication1 import *
from time import time

FILE = "2017Mar16"
DATA_PATH = 'Files\\'

# HUSK: at undgå split ved '-'

def parseSet(file = "SentimentAnalysisDataset"):
    clearfile("ds_pos")
    clearfile("ds_neg")
    time_start = time()
    print("Parsing set . . .")
    with open(getDataPath(file), "r", encoding='utf8') as f:
        k, max = 0, 20000
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
            with open(getDataPath(ds), "a") as fi:
                fi.write(prep(line[i:])[:-2] + "\n")
            k += 1


            if k % 1000 == 0:
                print("Finished " + str(k) + " of " + str(max))
            if k == max:
                break
    time_end = time()
    print("Processed " + FILE + " in " + (str)(time_end - time_start)[:4] + "s")

def process(file = FILE):
    time_start = time()
    data = open(getDataPath(file))
    clearfile()

    recent = [""] * 60
    index = 0

    for line in data:
        text = get_text(line)
        result = prep(text)
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


# prep
def prep(string):
    tokenized = tokenize(re.sub('[\']', '', string))
    result = ""
    for t in tokenized:
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
# is this needed?
def alter_prolonged(list = []):
    return


# clear file before writing
def clearfile(file = FILE):
    dp = getDataPath(file)[:-4] + "_p.txt"
    with open(dp, "w") as f:
        f.write("")

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