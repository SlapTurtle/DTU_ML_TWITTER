DATA_PATH = 'Files\\'
RAW_PATH = 'Raw\\'
PRE_PATH = 'Pre\\'
RES_PATH = 'Res\\'
FILTER_PATH = 'Filter\\'

FILE_tag = 'searchtags'
FILE_neu = "hneu_p"
FILE_pos = "hpos_p"
FILE_neg = "hneg_p"
FILE_bow_neu = 'neutrals'
FILE_bow_pos = 'positives'
FILE_bow_neg = 'negatives'

import os
import math

from dataGathering import *
from preprocessing import *
from analysis import *

def getTime():
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
	neuLines = []
	posLines = []
	negLines = []

	with open(getDataPath(FILE_neu), "r") as f:
		for line in f:
			neuLines.append([line.replace('\n',''),2])
	#print("Neutrals: " + str(len(neuLines)))

	with open(getDataPath(FILE_pos), "r") as f:
		for line in f:
			posLines.append([line.replace('\n',''),1])
	#print("Positives: " + str(len(posLines)))
	
	with open(getDataPath(FILE_neg), "r") as f:
		for line in f:
			negLines.append([line.replace('\n',''),0])
	#print("Negatives: " + str(len(negLines)))
	
	size = len(neuLines)+len(posLines)+len(negLines)
	
	if(size < totalSize):
		raise Exception('parameter \'totalSize\' is greater than the dataset')
	
	neusize = len(neuLines) / size * totalSize
	possize = len(posLines) / size * totalSize
	negsize = len(negLines) / size * totalSize

	#print("neu:" + str(neusize) + ", pos:" + str(possize) + ", neg:" + str(negsize))

	r.shuffle(neuLines)
	r.shuffle(posLines)
	r.shuffle(negLines)

	allLines = neuLines[:math.ceil(neusize)] + posLines[:math.ceil(possize)] + negLines[:math.ceil(negsize)]
	r.shuffle(allLines)
	allLines = allLines[:totalSize]

	testSize = int(testingSize*len(allLines))
	if testingSize == 0:
		train = allLines
		test = []
	else:
		train = allLines[:-testSize]
		test = allLines[-testSize:]    
	
	#print("TestSize: "+str(len(test)))
	#print("TrainSize: "+str(len(train)))

	return train,test

if __name__ == '__main__':
	#processDataSet()
	testModelScalingSimple()
	testModelScalingBayes()
	testModelScalingNeural()
	#startData()
	#train_neural_network()
	#testRandom()
	#bayesOnFolder(main.PRE_PATH)
	#bayesOnFolder(main.FILTER_PATH)
	#testBayes(size=1500);