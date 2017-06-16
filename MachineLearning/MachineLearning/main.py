# ---------------------------------------------------------------------
# These paths are the foldes the individual files are stored in 
# ---------------------------------------------------------------------
DATA_PATH = 'Files\\'
RAW_PATH = 'Raw\\'
PRE_PATH = 'Pre\\'
RES_PATH = 'Res\\'

# ---------------------------------------------------------------------
# These are the filenames of files used
# ---------------------------------------------------------------------
FILE_tag = 'searchtags'

FILE_neu_l = 'm_neu_large_p'
FILE_pos_l = 'm_pos_large_p' 
FILE_neg_l = 'm_neg_large_p'

FILE_neu_s = "hneu_p"
FILE_pos_s = "hpos_p"
FILE_neg_s = "hneg_p"

FILE_neu_bow = 'neutrals'
FILE_pos_bow = 'positives'
FILE_neg_bow = 'negatives'

# ---------------------------------------------------------------------
# Built-in packages
# ---------------------------------------------------------------------
import os
import math
import random as r
from time import time

# ---------------------------------------------------------------------
# Importing everything from the these three classes
# Also imports built-in packages used by those files
# ---------------------------------------------------------------------
from dataGathering import *
from preprocessing import *
from analysis import *

# ---------------------------------------------------------------------
# Methods used by all other files
# ---------------------------------------------------------------------

# Get the time, used to measure time used on certain methods
def getTime():
    return time()

# Finds the path where the program is stored
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

# Find a file with the '.txt' extension inside folders
def getDataPath(s, endtag='.txt'):
	path = directorySkip() + s + endtag
	return path

# Loads and seperates all lines in a file.
def loadFile(s, endtag='.txt'):
	list = []
	with open(getDataPath(s, endtag=endtag), "r") as file:
		for line in file:
			list.append(line.replace('\n', ''))
	return list

# Makes a randomized lexicon from the training set
def make_lexicon(testingSize, totalSize):
	if totalSize <= 1555:
		FILE_neu=FILE_neu_s
		FILE_pos=FILE_pos_s
		FILE_neg=FILE_neg_s
	else:
		FILE_neu=FILE_neu_l
		FILE_pos=FILE_pos_l
		FILE_neg=FILE_neg_l

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
	
	#print("Datasize: "+str(len(test)+len(train)))
	#print("TestSize: "+str(len(test)))
	#print("TrainSize: "+str(len(train)))

	return train,test

# Use the 1-gram Naive Bayes Method on all files in a folder
def bayesOnFolder(size=1555, readpath=PRE_PATH, writepath=RES_PATH, resname='_results'):
	pathread = main.directorySkip()+readpath
	pathwrite = main.directorySkip()+writepath

	_, _, filenames = next(os.walk(pathread))
	
	train, _ = main.make_lexicon(0,size)
	model = bayes.train_bayes(train)
	
	with open(pathwrite + resname + '.txt', "w") as f:
		f.write("")

	with open(pathwrite + resname + '.txt', "a") as f:
		for name in filenames:
			if(name != resname + '.txt'):
				data = loadFile(endpath+name, endtag='')
				neg,pos,neu,total = bayes.use_bayes(model, data, pathwrite+name[:-4])
				f.write(name[:-4] + ',' + str(neg) + ',' + str(pos) + ',' + str(neu) + ',' + str(total) + '\n')

# Use the 1-gram Naive Bayes Method on a single file, and dumps results to filepath
def use_bayes(model, data, filepath):
	res = test_bayes(model, data)
	dp = main.getDataPath(filepath, endtag='_b.txt')

	pos = 0
	neg = 0
	neu = 0

	with open(dp, "w") as f:
		f.write("")

	with open(dp, "a") as f:
		for clf in res:
			if clf == 2:
				neu += 1
			if clf == 1:
				pos += 1
			if clf == 0:
				neg += 1

			f.write(str(clf)+'\n')

	return neg,pos,neu,neg+pos+neu

# ---------------------------------------------------------------------
# Main process, used to execute the methods
# ---------------------------------------------------------------------
if __name__ == '__main__':
	#processDataSet()
	#testModelScalingSimple()
	testModelScalingBayes(1,1555,[1.0])
	#testModelScalingBayesSkipgram(count = 1, skip = 0, gram = 1)
	#testModelScalingBayesSkipgram(count = 1, skip = 0, gram = 2)
	#testModelScalingBayesSkipgram(count = 1, skip = 1, gram = 2)
	#testModelScalingBayesSkipgram(count = 1, skip = 2, gram = 2)
	#testModelScalingBayesSkipgram(count = 1, skip = 3, gram = 2)
	#testModelScalingBayesSkipgram(count = 1, skip = 4, gram = 2)
	#testModelScalingBayesSkipgram(count = 1, skip = 5, gram = 2)
	#testNeural(size = 1)
	#testModelScalingNeural(20)
	#testModelScalingAll()
	#testBayesSkipgramScaling(size = 1500000)
	#startData()
	#train_neural_network()