from PythonApplication1 import getDataPath,loadFile

def train_simple(pos,neg):
    print("---training simple")
    POSITIVES = set(loadFile(pos))
    NEGATIVES = set(loadFile(neg))

    return [POSITIVES,NEGATIVES]

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