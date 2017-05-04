#import tensorflow as tf
import os
from analysis import *
from semantics import *
from preprocessing import *
from dataGathering import *
#from bagofwords import *
from bayes import *

import random as r

DATA_PATH = 'Files\\'

FILE_pos = "ds_pos_p"
FILE_neg = "ds_neg_p"


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

def make_lexicon(testingSize, totalSize):
    print("---make lexicon")
    posLines = []
    negLines = []

    print("read posfile")
    with open(getDataPath(FILE_pos), "r") as f:
        for line in f:
            posLines.append([line.replace('\n',''),0])
    print(len(posLines))
    
    print("read negfile")
    with open(getDataPath(FILE_neg), "r") as f:
        for line in f:
            negLines.append([line.replace('\n',''),1])
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

    return correct/len(actualtest)

def testRandom(testingSize=0.1, size=1500000):
    train,test = make_lexicon(testingSize,size)

    results = []
    for _ in range(len(test)):
        results.append(r.randint(0,1))

    percent = compareResults(results, [row[1] for row in test])
    print(percent)

def testBayes(testingSize=0.1, size=1500000):
    train,test = make_lexicon(testingSize,size)
    model = train_bayes(train)
    results = test_bayes(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)

def testSimple(testingSize=0.1, size=1500000, pos="positives", neg="negatives"):
    train,test = make_lexicon(testingSize,size)
    model = train_simple(pos,neg)
    results = test_simple(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    print(percent)

def testAll(testingSize=0.1, size=1500000, pos="positives", neg="negatives"):
    eval = []

    train,test = make_lexicon(testingSize,size)

    print('--- testing random')
    results = []
    for _ in range(len(test)):
        results.append(r.randint(0,1))
    percent = compareResults(results, [row[1] for row in test])
    eval.append(['random', percent])

    model = train_simple(pos,neg)
    results = test_simple(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    eval.append(['simple', percent])

    model = train_bayes(train)
    results = test_bayes(model, [row[0] for row in test])
    percent = compareResults(results, [row[1] for row in test])
    eval.append(['bayes', percent])

    print(eval)

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