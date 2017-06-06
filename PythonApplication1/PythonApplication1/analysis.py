import PythonApplication1 as main
import random as r

from simple import *
from bayes import *
from neural import *

from os import walk

def testRandom(testingSize=0.1, size=1500000):
	train,test = main.make_lexicon(testingSize,size)
	model = None
	results = randomTest([row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	print(percent)

def testSimple(testingSize=0.1, size=1500000, neu=main.FILE_bow_neu, pos=main.FILE_bow_pos, neg=main.FILE_bow_neg):
	train,test = main.make_lexicon(testingSize,size)
	model = simple.train_simple(pos,neg)
	results = simple.test_simple(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	print(percent)

def testBayes(testingSize=0.1, size=1500000):
	train,test = main.make_lexicon(testingSize,size)
	model = train_bayes(train)
	results = test_bayes(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	#print(percent)
	return percent

def testNeural(testingSize=0.1, size=1500000, epochCount=10):
	train,test = main.make_lexicon(testingSize,size)
	return train_neural_network(train, test, epochCount)

def testAll(testingSize=0.1, size=1500000, neu=main.FILE_bow_neu, pos=main.FILE_bow_pos, neg=main.FILE_bow_neg, epochCount=10):
	eval = []

	train,test = main.make_lexicon(testingSize,size)

	model = None
	results = randomTest([row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	print(percent)
	eval.append(['random', percent])

	model = train_simple(neu, pos,neg)
	results = test_simple(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	print(percent)
	eval.append(['simple', percent])

	model = train_bayes(train)
	results = test_bayes(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	eval.append(['bayes', percent])

	percent = train_neural_network(train, test, epochCount)
	print(percent)
	eval.append(['neural', percent])

	print([testingSize, size, eval])
	return [testingSize, size, eval]

def compareResults(modeltest, actualtest):
	#print("---comparing results")
	correct = 0
	for r1,r2 in zip(modeltest,actualtest):
		if r1==r2:
			correct += 1

	return correct / len(actualtest)

def randomTest(data):
	print('---testing random')
	results = []
	for _ in range(len(data)):
		results.append(r.randint(0,2))
	return results

def bayesOnFolder(endpath):
	path=main.directorySkip()+endpath
	
	_, _, filenames = next(walk(path))
	
	train, _ = main.make_lexicon(0,1500000)
	model = train_bayes(train)
	
	path += '_results.txt'
	with open(path, "w") as f:
		f.write("")

	with open(path, "a") as f:
		for name in filenames:
			if(name != '_results.txt'):
				data = main.loadFile(endpath+name, endtag='')
				neg,pos,neu,total = use_bayes(model, data, name[:-4])
				f.write(name[:-4] + ',' + str(neg) + ',' + str(pos) + ',' + str(neu) + ',' + str(total) + '\n')