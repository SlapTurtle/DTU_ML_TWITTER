DATA_PATH = 'Files\\'
RAW_PATH = 'Raw\\'
PRE_PATH = 'Pre\\'
RES_PATH = 'Res\\'
FILTER_PATH = 'Filter\\'

FILE_tag = 'searchtags'
FILE_neu = "ds_neu_p"
FILE_pos = "ds_pos_p"
FILE_neg = "ds_neg_p"
FILE_bow_neu = 'neutrals'
FILE_bow_pos = 'positives'
FILE_bow_neg = 'negatives'

import os

from dataGathering import *
from preprocessing import *
from analysis import *

def time():
    return time()

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

def loadFile(s, endtag='.txt'):
	list = []
	with open(getDataPath(s, endtag=endtag), "r") as file:
		for line in file:
			list.append(line.replace('\n', ''))
	return list

def make_lexicon(testingSize, totalSize):
	print("---make lexicon")
	neuLines = []
	posLines = []
	negLines = []

	print("read neufile")
	with open(getDataPath(FILE_neu), "r") as f:
		for line in f:
			neuLines.append([line.replace('\n',''),2])
	print(len(neuLines))

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
	allLines = neuLines+posLines+negLines
	r.shuffle(allLines)

	print("cuts testsize")
	allLines = allLines[:totalSize]
	print(len(allLines))

	if testingSize == 0:
		train = allLines
		test = []
	else:
		testSize = int(testingSize*len(allLines))
		train = allLines[:-testSize]
		test = allLines[-testSize:]    
	
	print("TestSize: "+str(len(test)))
	print("TrainSize: "+str(len(train)))

	print("return: train test")
	return train,test

if __name__ == '__main__':
	#parseSet()
	#process()
	#startData()
	#analysis()
	#train_neural_network()

	#testRandom()
	#testSimple()
	#testBayes()
	testAll(size = 10000)

	#bayesOnFolder(main.PRE_PATH)
	#bayesOnFolder(main.FILTER_PATH)