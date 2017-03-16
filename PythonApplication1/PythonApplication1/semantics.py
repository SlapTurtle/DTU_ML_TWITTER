from PythonApplication1 import *
from preprocessing import *
from time import time
from searchPosNeg import *

FILE = ""
POSITIVES = []
NEGATIVES = []
TRIE = []

def semantics(s):
    global POSITIVES, NEGATIVES, FILE, TRIE
    FILE = s
    data = open(getDataPath(FILE))
    POSITIVES = set(loadLexicon("positives"))
    NEGATIVES = set(loadLexicon("negatives"))

    #TRIE = getSearchTrie()

    time_start = time()
    positives = 0
    negatives = 0
    total = 0

    for line in data:
        try:
            result = evaluate(line)
            if result > 0:
                positives = positives + 1
            elif result < 0:
                negatives = negatives + 1
            total = total + 1
        except:
            pass

    time_finish = time()
    print("\nFinished in " + str(time_finish - time_start)[:4] + "s with the following result:")
    print("Positives: " + str(positives) + " (" + str((positives/total)*100)[:4] + "%)")
    print("Negatives: " + str(negatives) + " (" + str((negatives/total)*100)[:4] + "%)")
    print("Total tweets: " + str(total))
    print("Overall score: " + str(positives - negatives) + "\n")

def evaluate(line):
    list = line.split()
    positives = 0
    negatives = 0
    total = len(list)

    for word in list:
        #search = TRIE.search(word)
        #if search == True:
        #    positives = positives + 1
        #elif search == False:
        #    negatives = negatives + 1
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
