import nltk
from nltk.corpus import brown
from PythonApplication1 import *
from preprocessing import *
from time import time

FILE = ""
POSITIVES = set()
NEGATIVES = set()
SEARCHTAGS = set()


def semantics(s):
    global POSITIVES, NEGATIVES, FILE, SEARCHTAGS
    FILE = s
    data = open(getDataPath(FILE))
    POSITIVES = set(loadLexicon("positives"))
    NEGATIVES = set(loadLexicon("negatives"))
    SEARCHTAGS = getSearchTags()

    evaluation = []
    time_start = time()
    positives = 0
    negatives = 0
    total = 0

    for line in data:
        try:
            result = evaluate(line)
            evaluation.append(result)
            if result > 0:
                positives = positives + 1
            elif result < 0:
                negatives = negatives + 1
            total = total + 1
        except:
            pass

    time_finish = time()
    print("\nFinished in " + str(time_finish - time_start)[:4] + "s with the following result:\n")
    print("Positives: " + str(positives) + " (" + str((positives/total)*100)[:4] + "%)")
    print("Negatives: " + str(negatives) + " (" + str((negatives/total)*100)[:4] + "%)")
    print("Total tweets: " + str(total))
    print("Overall score: " + str(positives - negatives) + "\n")
    return evaluation

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


def identify(s):
    print("Analysing: " + str(s))
    tokens = nltk.word_tokenize(s)
    tagged = nltk.pos_tag(tokens)

    print(tagged)
    return tagged


def loadLexicon(s):
    list = []
    with open(getDataPath(s), "r") as file:
        for line in file:
            list.append(line[:-1])
    return list
