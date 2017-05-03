from PythonApplication1 import *
from collections import Counter

FILE_pos = "ds_pos_p"
FILE_neg = "ds_neg_p"

def make_lexicon(testingSize):
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

    testSize = int(testingSize*len(allLines))
    train = allLines[:-testSize]
    test = allLines[-testSize:]
    print("TestSize: "+str(len(test)))
    print("TrainSize: "+str(len(train)))

    print("return: train test")
    return train,test

def train_model(data):
    print("---train model")
    posWords = []
    negWords = []

    print("making wordlists")
    for line,clf in data:
        if clf == 0:
            posWords.extend(line.split(' '))
        elif clf == 1:
            negWords.extend(line.split(' '))
        else:
            print('ERROR')

    print("counting words")
    posSet = Counter(posWords)
    negSet = Counter(negWords)

    allSet = set(posWords+negWords)
    count = len(allSet)

    print("making dict")
    lexicon = dict()
    for word in allSet:
        if word not in posSet:
            posSet[word] = 0
        if word not in negSet:
            negSet[word] = 0
        lexicon[word] = [posSet[word]/count,negSet[word]/count]

    print("returning model")
    return lexicon

def test_model(model, data):
    print("---testing model")

    print("testing samples")
    results = []
    for line,clf in data:
        res = single_sample(model, line)
        results.append([res,clf])
    
    print("comparing results")
    correct = 0
    for r1,r2 in results:
        if r1==r2:
            correct += 1

    return correct/len(results)

def single_sample(model, line):
    words = line.split(' ')
    cp = [1/3, 1/3]
    for clf in range(len(cp)):
        for word in words:
            if word in model:
                cp[clf] *= model[word][clf]

    return cp.index(max(cp)) 

def run_bayes(testingSize=0.1):

    train,test = make_lexicon(testingSize)
    model = train_model(train)
    results = test_model(model, test)

    print(results)

