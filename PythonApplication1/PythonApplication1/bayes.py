from collections import Counter

def train_bayes(data):
    print("---train bayes")
    posWords = []
    negWords = []

    print("making wordlists")
    for line,clf in data:
        if clf == 1:
            posWords.extend(line.split(' '))
        elif clf == 0:
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
        lexicon[word] = [negSet[word]/count,posSet[word]/count]

    print("returning model")
    return lexicon

def test_bayes(model, data):
    print("---testing bayes")

    print("testing samples")
    results = []
    for line in data:
        res = single_sample_bayes(model, line)
        results.append(res)

    print("returning results")
    return results

def single_sample_bayes(model, line):
    words = line.split(' ')
    cp = [1/2, 1/2]
    for clf in range(len(cp)):
        for word in words:
            if word in model:
                cp[clf] *= model[word][clf]

    return cp.index(max(cp)) 