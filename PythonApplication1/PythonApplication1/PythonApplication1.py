#import tensorflow as tf
import os
from analysis import *
from semantics import *
from preprocessing import *
from searchPosNeg import *
from dataGathering import *

DATA_PATH = 'Files\\'

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

def getDataPath(s):
    path = directorySkip() + s +'.txt'
    return path

if __name__ == '__main__':
    #process()
    #getSearchTrie()
    #startData()
    analysis()