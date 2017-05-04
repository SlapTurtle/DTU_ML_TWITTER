from PythonApplication1 import getDataPath

def train_simple(pos,neg):
    print("---training simple")
    POSITIVES = set(loadLexicon(pos))
    NEGATIVES = set(loadLexicon(neg))

    return [POSITIVES,NEGATIVES]

def loadLexicon(s):
    list = []
    with open(getDataPath(s), "r") as file:
        for line in file:
            list.append(line.replace('\n', ''))
    return list

def test_simple(model, data):
    print("---testing simple")
    results = []
    for line in data:
        res = single_sample_simple(model, line)
        results.append(res)

    return results

def single_sample_simple(model, line):
    words = line.split(' ')
    positives = 0
    negatives = 0

    for word in words:
        if word in model[0]:
            positives = positives + 1
        elif word in model[1]:
            negatives = negatives + 1
    
    return 0 if (positives >= negatives) else 1


