import re
from string import digits
from PythonApplication1 import *

FILE = "2017Mar06"

# HUSK: at undgå split ved '-'

def process():
    data = open(getDataPath(FILE))
    clearfile()

    recent = ["", "", "", "", ""]
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
            print(result)
            print("\n")
            filedump(result + "\n")
            recent[index] = result
            if (1 + index < len(recent)):
                index = index + 1
            else:
                index = 0


# get text from data string
def get_text(string):
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
        if (word == "https"):
            for j in range(0,4):
                tokenized.pop(i)
        elif (len(word) < 2) or (len(word) <= 3 and word[0] == 'x') or (word == "rt"):
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