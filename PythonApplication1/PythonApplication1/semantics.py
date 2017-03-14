from PythonApplication1 import *
from preprocessing import *

FILE = "2017Mar08"
POSITIVES = []
NEGATIVES = []

def semantics():
    global POSITIVES, NEGATIVES
    print("Running Semantics...")
    data = open(getDataPath(FILE))
    POSITIVES = set(loadLexicon("positives"))
    NEGATIVES = set(loadLexicon("negatives"))

    positives = 0
    negatives = 0

    for line in data:
        result = evaluate(line)
        if result > 0:
            positives = positives + 1
        elif result < 0:
            negatives = negatives + 1
        #filedump(evaluate(line))

    print("Positives: " + str(positives))
    print("Negatives: " + str(negatives))
    print("Overall score: " + str(positives - negatives))

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
