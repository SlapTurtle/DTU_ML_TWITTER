# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
import main

import simple
import bayes
import bayes_skipgram
import neural

# ---------------------------------------------------------------------
# Model Performance Analysis
# ---------------------------------------------------------------------

# Tests how the accuary scales with differetn k-skin-n-gram values
# count = average accuracy of XX runs
# size = size to be traied on
def testBayesSkipgramScaling(count, size):
	p = 0
	for i in range(count):
		p += testbayesskipgram(size = size, skip = 0, gram = 1)
	p = p/count
	print("bayes0s1g, size = "+str(size)+", accuracy="+str(p) + ", avg. of "+str(count)+" runs")

	for j in range(2,3):
		for i in range(5,10):
			p = 0
			for k in range(count):
				p += testBayesSkipgram(size = size, skip=i, gram=j)
			p = p/count
			print("bayes"+str(i)+"S"+str(j)+"G, size = "+str(size)+", accuracy="+str(p) + ", avg. of "+str(count)+" runs")

# Tests how the simple model scales on training size
# count = average accuracy of XX runs
# max = maximum size to be traied on
# value = the percentages to be tested, for instance [0.05, 0.10, 0.25, 0.50, 0.75, 1.00]
def testModelScalingSimple(count, max, values):
	print("------Simple------")
	for p in values:
		x = int(p*max)
		j = 0
		for i in range(count):
			j += testSimple(size = max, percent = p )
		j = j/count
		print("size = " + str(6784*p) + ", accuracy = " + str(j)  + ", avg. of "+str(count)+" runs")
	print("-----------------")

# Tests how the 1-gram Naive Bayes model scales on training size
# count = average accuracy of XX runs
# max = maximum size to be traied on
# value = the percentages to be tested, for instance [0.05, 0.10, 0.25, 0.50, 0.75, 1.00]
def testModelScalingBayes(count, max, values):
	print("------Bayes------")
	for p in values:
		x = int(max*p)
		j = 0
		for i in range(count):
			k = testBayes(size = x)
			j += k
		j = j/count
		print("size = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	print("-----------------")

# Tests how the k-skip-n-gram Naive Bayes model scales on training size
# count = average accuracy of XX runs
# max = maximum size to be traied on
# value = the percentages to be tested, for instance [0.05, 0.10, 0.25, 0.50, 0.75, 1.00]
# skip = k-skip value
# gram = n-gram value
def testModelScalingBayesSkipgram(count, max, values, skip, gram):
	print("----Bayes"+str(skip)+"S"+str(gram)+"G----")
	for p in values:
		x = int(max*p)
		j = 0
		for i in range(count):
			k = testBayesSkipgram(size = x, skip=skip, gram=gram)
			j += k
		j = j/count
		print("sizeSimple = "+str(x)+", size = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	print("-----------------")

# Tests how the Neural Netowrk model scales on training size
# count = average accuracy of XX runs
# max = maximum size to be traied on
# value = the percentages to be tested, for instance [0.05, 0.10, 0.25, 0.50, 0.75, 1.00]
def testModelScalingNeural(count, max, values):
	print("------Neural------")
	for p in values:
		x = int(max*p)
		j = 0
		for i in range(count):
			k = testNeural(x)
			j += k
		j = j/count
		print("size = " + str(x) + ", accuracy = " + str(j) + ", avg. of "+str(count)+" runs")
	print("-----------------")

# Tests how all the model scales on training size
# count = average accuracy of XX runs
# max = maximum size to be traied on
# value = the percentages to be tested, for instance [0.05, 0.10, 0.25, 0.50, 0.75, 1.00]
# skip = k-skip value
# gram = n-gram value
def testModelScalingAll(count, max, values, skip, gram):
	for p in values:
		x = int(max*p)
		j = 0
		j = [0,0,0,0]
		for i in range(count):
			list = testAll(x, p, skip, gram)
			for k in range(1, len(j)):
				j[k] += list[2][k-1][1]
		for k in range(0, len(j)):
			j[k] = j[k]/count
		print("sizeSimple = "+str(6784*p)+", size = " + str(x) + ", accuracy(s,b,bs"+str(skip)+"g"+str(gram)+",n) = " + str(j) + ", avg. of "+str(count)+" runs")

# Performs a single simple performance analysis
def testSimple(size, percent, testingSize=0.1, neu=main.FILE_neu_bow, pos=main.FILE_pos_bow, neg=main.FILE_neg_bow):
	train,test = main.make_lexicon(testingSize,size)
	#time_start = main.getTime()
	model = simple.train_simple(neg,pos,neu,percent)
	#time_1 = main.getTime()
	#print("Simple train time elapsed: " + str(time_1 - time_start))
	results = simple.test_simple(model, [row[0] for row in test])
	#time_end = main.getTime()
	#print("Simple test time elapsed: " + str(time_end - time_1))
	percent = compareResults(results, [row[1] for row in test])
	return percent

# Performs a single 1-gram bayes performance analysis
def testBayes(size, testingSize=0.1):
	train,test = main.make_lexicon(testingSize,size)
	#time_start = main.getTime()
	model = bayes.train_bayes(train)
	#time_1 = main.getTime()
	#print("Bayes train time elapsed: " + str(time_1 - time_start))
	results = bayes.test_bayes(model, [row[0] for row in test])
	#time_end = main.getTime()
	#print("Bayes test time elapsed: " + str(time_end - time_1))
	percent = compareResults(results, [row[1] for row in test])
	return percent

# Performs a single k-skip-n-gram bayes performance analysis
def testBayesSkipgram(size, skip, gram, testingSize=0.1):
	train,test = main.make_lexicon(testingSize,size)
	#time_start = main.getTime()
	model = bayes_skipgram.train_bayes_skipgram(train, skip, gram)
	#time_1 = main.getTime()
	#print("Bayes"+str(skip)+"S"+str(gram)+"G train time elapsed: " + str(time_1 - time_start))
	results = bayes_skipgram.test_bayes_skipgram(model, [row[0] for row in test], skip, gram)
	#time_end = main.getTime()
	#print("Bayes"+str(skip)+"S"+str(gram)+"G test time elapsed: " + str(time_end - time_1))
	percent = compareResults(results, [row[1] for row in test])
	return percent

# Performs a single Neural Network performance analysis
def testNeural(size, testingSize=0.1):
	train,test = main.make_lexicon(testingSize,size)
	return neural.train_neural_network(train, test)

# Performs a single performance analysis of all models
def testAll(size, percent, skip, gram, epochCount, testingSize=0.1, neu=main.FILE_neu_bow, pos=main.FILE_pos_bow, neg=main.FILE_neg_bow):
	eval = []

	train,test = main.make_lexicon(testingSize,size)

	model = simple.train_simple(neg,pos,neu,percent)
	results = simple.test_simple(model, [row[0] for row in test])
	p = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(['simple', p])

	model = bayes.train_bayes(train)
	results = bayes.test_bayes(model, [row[0] for row in test])
	p = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(["bayesS"+str(skip)+"G"+str(gram), p])

	model = bayes_skipgram.train_bayes_skipgram(train, skip, gram)
	results = bayes_skipgram.test_bayes_skipgram(model, [row[0] for row in test], skip, gram)
	p = compareResults(results, [row[1] for row in test])
	#print(percent)
	eval.append(['bayes', p])

	p = neural.train_neural_network(train, test, epochCount)
	#print(percent)
	eval.append(['neural', p])

	#print(str([testingSize, size, eval]))
	return [testingSize, size, eval]

# Evaluates the results of testing a trained model
def compareResults(testresults, labels):
	correct = 0
	for r1,r2 in zip(testresults, labels):
		if r1==r2:
			correct += 1
	#print(correct / len(labels))
	return correct / len(labels)