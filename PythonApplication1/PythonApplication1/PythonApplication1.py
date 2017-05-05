import os

from dataGathering import *
from preprocessing import *

from simple import *
from bayes import *
from neural import *

import random as r

DATA_PATH = 'Files\\'
RAW_PATH = 'Raw\\'
PRE_PATH = 'Pre\\'

FILE_tag = 'searchtags'
FILE_pos = "ds_pos_p"
FILE_neg = "ds_neg_p"
FILE_bow_pos = 'positives'
FILE_bow_neg = 'negatives'


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

def getDataPath(s, endtag='.txt'):
    path = directorySkip() + s + endtag
    return path

def loadFile(s):
    list = []
    with open(getDataPath(s), "r") as file:
        for line in file:
            list.append(line.replace('\n', ''))
    return list

def make_lexicon(testingSize, totalSize):
    print("---make lexicon")
    posLines = []
    negLines = []

    print("read posfile")
    with open(getDataPath(FILE_pos), "r") as f:
        for line in f:
            posLines.append([line.replace('\n',''),1])
    print(len(posLines))
    
    print("read negfile")
    with open(getDataPath(FILE_neg), "r") as f:
        for line in f:
            negLines.append([line.replace('\n',''),0])
    print(len(negLines))

    print("shuffle all")
    allLines = posLines+negLines
    r.shuffle(allLines)

    print("cuts testsize")
    allLines = allLines[:totalSize]
    print(len(allLines))

    testSize = int(testingSize*len(allLines))
    train = allLines[:-testSize]
    test = allLines[-testSize:]
    print("TestSize: "+str(len(test)))
    print("TrainSize: "+str(len(train)))

    print("return: train test")
    return train,test

def compareResults(modeltest, actualtest):
    print("---comparing results")
    correct = 0
    for r1,r2 in zip(modeltest,actualtest):
        if r1==r2:
            correct += 1

    return correct / len(actualtest)

def randomTest(data):
    print('---testing random')
    results = []
    for _ in range(len(data)):
        results.append(r.randint(0,1))
    return results

def testRandom(testingSize=0.1, size=1500000):
    train,test = make_lexicon(testingSize,size)
    model = None
    results = randomTest([row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)

def testSimple(testingSize=0.1, size=1500000, pos=FILE_bow_pos, neg=FILE_bow_neg):
    train,test = make_lexicon(testingSize,size)
    model = train_simple(pos,neg)
    results = test_simple(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)

def testBayes(testingSize=0.1, size=1500000):
    train,test = make_lexicon(testingSize,size)
    model = train_bayes(train)
    results = test_bayes(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)

def testNeural(testingSize=0.1, size=1500000, epochCount=10):
    train,test = make_lexicon(testingSize,size)
    train_neural_network(train, test, epochCount)

def testAll(testingSize=0.1, size=100000, pos=FILE_bow_pos, neg=FILE_bow_neg, epochCount=10):
    eval = []

    train,test = make_lexicon(testingSize,size)

    model = None
    results = randomTest([row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)
    eval.append(['random', percent])

    model = train_simple(pos,neg)
    results = test_simple(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)
    eval.append(['simple', percent])

    model = train_bayes(train)
    results = test_bayes(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    eval.append(['bayes', percent])

    percent = train_neural_network(train, test, epochCount)
    print(percent)
    eval.append(['neural', percent])

    print([testingSize, size, eval])
    return [testingSize, size, eval]

if __name__ == '__main__':
    #parseSet()
    #process()
    #startData()
    #analysis()
    #train_neural_network()

    #testRandom()
    #testSimple()
    #testBayes()
    testAll()