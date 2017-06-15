import PythonApplication1 as main
import random as r

import simple
import bayes
import bayes_skipgram
import neural

from os import walk

def testBayesSkipgramScaling(count = 1, size = 1500000):
	#p = 0
	#for i in range(count):
	#	p += testBayesSkipgram(size = size, skip = 0, gram = 1)
	#p = p/count
	#print("bayes0S1G, size = "+str(size)+", accuracy="+str(p) + ", avg. of "+str(count)+" runs")

	for j in range(2,5):
		for i in range(2,5):
			p = 0
			for k in range(count):
				p += testBayesSkipgram(size = size, skip=i, gram=j)
			p = p/count
			print("bayes"+str(i)+"S"+str(j)+"G, size = "+str(size)+", accuracy="+str(p) + ", avg. of "+str(count)+" runs")

def testModelScalingSimple(count = 100):
	p = []
	for x in range(1, 17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			j += testSimple(size = x, percent = x/1555 )
		j = j/count
		#print("size = " + str(x/1555*6784) + ", accuracy = " + str(j)  + ", avg. of "+str(count)+" runs")
		p.append((x,j))
	print("------Simple------")
	for x,j in p:
		print("size = " + str(x/1555*6784) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	print("-----------------")

def testModelScalingBayes(count = 100):
	#p = []
	print("------Bayes------")
	for x in range(1,17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			k = testBayes(size = x)
			j += k
			#print(k, end=', ')
		j = j/count
		print('\n', "size = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
		#p.append((x,j))
	#for x,j in p:
	#	print("size = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	print("-----------------")

def testModelScalingBayesSkipgram(count = 100, skip=1, gram=2):
	#p = []
	print("----Bayes"+str(skip)+"S"+str(gram)+"G----")
	for x in range(1,17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			k = testBayesSkipgram(size = x, skip=skip, gram=gram)
			j += k
		j = j/count
		print("size = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
		#p.append((x,j))
	#for x,j in p:
	#	print("size = " + str(x) + ", accuracy = " + str(j)  + ", avg. of "+str(count)+" runs")
	print("-----------------")

def testModelScalingNeural(count = 10):
	#p = []
	print("------Neural------")
	for x in range(10,17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = 0
		for i in range(count):
			k = testNeural(size = x)
			j += k
		j = j/count
		print("x = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	#	p.append((x,j))
	#for x,j in p:
	#	print("x = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	print("-----------------")

def testModelScalingAll(count=10, skip=1, gram=2):
	p = []
	for x in range(1,17):
		if x < 16:
			x *= 100
		else:
			x = 1555
		j = [0,0,0,0,0]
		for i in range(count):
			list = testAll(size=x, pc=x/1555, skip=skip, gram=gram)
			for k in range(len(j)):
				j[k] += list[2][k][1]
		for k in range(len(j)):
			j[k] = j[k]/count
		print("size = " + str(x) + ", accuracy(r,s,b,bs"+str(skip)+"g"+str(gram)+",n) = " + str(j) + ", avg. of "+str(count)+" runs")

def testRandom(testingSize=0.1, size=1555):
	train,test = main.make_lexicon(testingSize,size)
	model = None
	results = []
	for _ in range(len(test)):
		results.append(r.randint(0,2))
	percent = compareResults(results, [row[1] for row in test])
	print(percent)

def testSimple(testingSize=0.1, size=1555, percent=1.0, neu=main.FILE_bow_neu, pos=main.FILE_bow_pos, neg=main.FILE_bow_neg):
	train,test = main.make_lexicon(testingSize,size)
	model = simple.train_simple(neg,pos,neu,percent)
	results = simple.test_simple(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	return percent

def testBayes(testingSize=0.1, size=1555):
	train,test = main.make_lexicon(testingSize,size)
	model = bayes.train_bayes(train)
	results = bayes.test_bayes(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	return percent

def testBayesSkipgram(testingSize=0.1, size=1555, skip=1, gram=2):
	train,test = main.make_lexicon(testingSize,size)
	time_start = main.getTime()
	model = bayes_skipgram.train_bayes_skipgram(train, skip, gram)
	time_1 = main.getTime()
	print("Bayes time elapsed: " + str(time_1 - time_start))
	results = bayes_skipgram.test_bayes_skipgram(model, [row[0] for row in test], skip, gram)
	time_end = main.getTime()
	print("Bayes time elapsed: " + str(time_end - time_1))
	percent = compareResults(results, [row[1] for row in test])
	return percent

def testNeural(testingSize=0.1, size=1555, epochCount=20):
	train,test = main.make_lexicon(testingSize,size)
	return neural.train_neural_network(train, test, epochCount)

def testAll(testingSize=0.1, size=1555, pc=1.0, neu=main.FILE_bow_neu, pos=main.FILE_bow_pos, neg=main.FILE_bow_neg, skip=1, gram=2, epochCount=10):
	eval = []

	train,test = main.make_lexicon(testingSize,size)
	
	model = None
	results = []
	for _ in range(len(test)):
		results.append(r.randint(0,2))
	percent = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(['random', percent])

	model = simple.train_simple(neg,pos,neu,pc)
	results = simple.test_simple(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(['simple', percent])

	model = bayes.train_bayes(train)
	results = bayes.test_bayes(model, [row[0] for row in test])
	percent = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(["bayesS"+str(skip)+"G"+str(gram), percent])

	model = bayes_skipgram.train_bayes_skipgram(train, skip, gram)
	results = bayes_skipgram.test_bayes_skipgram(model, [row[0] for row in test], skip, gram)
	percent = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(['bayes', percent])

	percent = neural.train_neural_network(train, test, epochCount)
	#print(percent)
	eval.append(['neural', percent])

	#print(str([testingSize, size, eval]))
	return [testingSize, size, eval]

def compareResults(modeltest, actualtest):
	#print("---comparing results")
	correct = 0
	for r1,r2 in zip(modeltest,actualtest):
		if r1==r2:
			correct += 1

	return correct / len(actualtest)

def bayesOnFolder(endpath):
	path=main.directorySkip()+endpath
	
	_, _, filenames = next(walk(path))
	
	train, _ = main.make_lexicon(0,1555)
	model = bayes.train_bayes(train)
	
	path += '_results.txt'
	with open(path, "w") as f:
		f.write("")

	with open(path, "a") as f:
		for name in filenames:
			if(name != '_results.txt'):
				data = main.loadFile(endpath+name, endtag='')
				neg,pos,neu,total = bayes.use_bayes(model, data, name[:-4])
				f.write(name[:-4] + ',' + str(neg) + ',' + str(pos) + ',' + str(neu) + ',' + str(total) + '\n')