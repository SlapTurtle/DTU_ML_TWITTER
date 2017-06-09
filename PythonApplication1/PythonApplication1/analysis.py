import PythonApplication1 as main
import random as r

import simple as simple
from bayes import *
from neural import *

from os import walk

def testModelScalingSimple():
	p = []
	count = 100
	for x in range(1, 17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			j += testSimple(size = x)
		j = j/count
		print("x = " + str(x) + ", accuracy = " + str(j))
		p.append((x,j))
	print("------Simple------")
	for x,j in p:
		print("x = " + str(x) + ", accuracy = " + str(j) +", average of " + str(count) + " tries")
	print("-----------------")

def testModelScalingBayes():
	p = []
	count = 100
	for x in range(1,17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			j += testBayes(size = x)
		j = j/count
		print("x = " + str(x) + ", accuracy = " + str(j))
		p.append((x,j))
	print("------Bayes------")
	for x,j in p:
		print("x = " + str(x) + ", accuracy = " + str(j) +", average of " + str(count) + " tries")
	print("-----------------")

def testModelScalingNeural():
	p = []
	count = 10
	for x in range(1,17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			j += testNeural(size = x)
		j = j/count
		print("x = " + str(x) + ", accuracy = " + str(j))
		p.append((x,j))
	print("------Neural------")
	for x,j in p:
		print("x = " + str(x) + ", accuracy = " + str(j) +", average of " + str(count) + " tries")
	print("-----------------")

def testRandom(testingSize=0.1, size=1500000):
	train,test = main.make_lexicon(testingSize,size)
	model = None
	results = randomTest([row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	print(percent)

def testSimple(testingSize=0.1, size=1500000, neu=main.FILE_bow_neu, pos=main.FILE_bow_pos, neg=main.FILE_bow_neg):
	train,test = main.make_lexicon(testingSize,size)
	model = simple.train_simple(neg,pos,neu)
	results = simple.test_simple(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	return percent

def testBayes(testingSize=0.1, size=1500000):
	train,test = main.make_lexicon(testingSize,size)
	model = train_bayes(train)
	results = test_bayes(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
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