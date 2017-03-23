from semantics import *
from preprocessing import *

FILE = "testdata"


def analysis():
    #full_analysis()
    res = analyze(FILE + "_p")
    accuracy(res)
    print("\n")
    #identify("I hate Apple, because Microsoft has better products")


def full_analysis():
    print("Yet to be implemented")


def analyze(s):
    print("Semantics analysis for " + FILE + " . . .")
    return semantics(s)


def accuracy(data):
    manual = open(getDataPath(FILE + "_s"))
    correct = 0
    total = 0
    m_pos = 0
    m_neg = 0
    i = 0

    for line in manual:
        if int(line) > 0:
            m_pos = m_pos + 1
        elif int(line) < 0:
            m_neg = m_neg + 1
        res = 0
        if data[i] > 0:
            res = 1
        elif data[i] < 0:
            res = -1
        if res == int(line):
            correct = correct + 1
        total = total + 1
        i = i + 1

    print("Accuracy: " + str(correct) + " of " + str(total))
    print("Actual Positives: " + str(m_pos) + " (" + str((m_pos / total) * 100) + "%),  Negatives: " + str(m_neg) + " (" + str((m_neg / total) * 100) + "%)")