import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
import random
from collections import Counter

fixedPath = 'C:\\Users\\Michael\\Source\\Repos\\DTU_ML_TWITTER\\Files\\2017Mar16_p.txt'
Lemmatizer = WordNetLemmatizer()

def create_lexicon(allFilePaths):
    retLex = dict()
    tmpLex = []

    for filepath in allFilePaths:
        with open(filepath, 'r') as f:
            for line in f:
                nl = line.replace('\n','')
                nl = nl.split(' ')
                for word in nl:
                    tmpLex += [word]
    
    print(tmpLex)
    tmpLex = [Lemmatizer.lemmatize(i) for i in tmpLex]
    print(tmpLex)
    wordcount = Counter(tmpLex)
    for word in wordcount:
        # chance values
        if 10000 > wordcount[word] > 10:
            retLex[word] = wordcount[word]
    
    return retLex

def sample_handling(sampleString, lexicon, classicitation):
    np.zeros(len(lexicon))
    return None

def testLex():
    print(create_lexicon([fixedPath]))





    


