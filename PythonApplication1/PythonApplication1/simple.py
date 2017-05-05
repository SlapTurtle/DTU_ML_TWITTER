import PythonApplication1 as main

def train_simple(pos,neg):
    print("---training simple")
    POSITIVES = set(main.loadFile(pos))
    NEGATIVES = set(main.loadFile(neg))

    return [POSITIVES,NEGATIVES]

def test_simple(model, data):
    print("---testing simple")
    results = []
    for line in data:
        res = single_sample_simple(model, line)
        results.append(res)

    return results

def single_sample_simple(model, line):
    score = 0

    words = line.split(' ')
    for word in words:
        if word in model[0]:
            score += 1
        elif word in model[1]:
            score -= 1

    return 1 if score >= 0 else 0