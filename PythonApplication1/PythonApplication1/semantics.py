from PythonApplication1 import *
from preprocessing import *

FILE = "testdata"
POSITIVES = []
NEGATIVES = []

def semantics():
    global POSITIVE, NEGATIVES
    print("Running Semantics...")
    data = open(getDataPath(FILE))
    POSITIVES = set(loadLexicon("positives"))
    NEGATIVES = set(loadLexicon("negatives"))

    for line in data:
        result = evaluate(line)
        print(result)
        #filedump(evaluate(line))


def evaluate(line):
    list = line.split()
    positives = 0
    negatives = 0
    total = len(list)

    for word in list:
        if word in POSITIVES:
            positives = positives + 1
        elif word in NEGATIVES:
            negatives = negatives + 1
    
    return positives - negatives

def loadLexicon(s):
    list = []
    with open(getDataPath(s), "r") as file:
        for line in file:
            list.append(line[:-1])
    return list
