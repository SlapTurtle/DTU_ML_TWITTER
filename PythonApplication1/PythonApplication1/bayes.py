import PythonApplication1 as main
from collections import Counter

def train_bayes(data):
	#print("---train bayes")
	negWords = []
	posWords = []
	neuWords = []

	#print("making wordlists")
	for line,clf in data:
		if clf == 2:
			neuWords.extend(line.split(' '))
		elif clf == 1:
			posWords.extend(line.split(' '))
		elif clf == 0:
			negWords.extend(line.split(' '))
		else:
			print('ERROR')

	#print("counting words")
	neuSet = Counter(neuWords)
	posSet = Counter(posWords)
	negSet = Counter(negWords)

	allSet = set(negWords+posWords+neuWords)
	count = len(allSet)

	#print("making dict")
	lexicon = dict()
	for word in allSet:
		if word not in neuSet:
			neuSet[word] = 0
		if word not in posSet:
			posSet[word] = 0
		if word not in negSet:
			negSet[word] = 0
		lexicon[word] = [negSet[word]/count,posSet[word]/count,neuSet[word]/count]

	#print("returning model")
	return lexicon

def test_bayes(model, data):
	#print("---testing bayes")
	#print("testing samples")
	results = []
	time_start = main.getTime()
	for line in data:
		res = single_sample_bayes(model, line)
		results.append(res)
	time_end = main.getTime()
	#print("Bayes time elapsed: " + str(time_end - time_start))
	#print("returning results")
	return results

def single_sample_bayes(model, line):
	words = line.split(' ')
	cp = [1/3, 1/3, 1/3]
	for clf in range(len(cp)):
		for word in words:
			if word in model:
				cp[clf] *= model[word][clf]

	return cp.index(max(cp))

def use_bayes(model, data, filename):
	res = test_bayes(model, data)
	dp = main.getDataPath(main.RES_PATH + filename, endtag='_b.txt')

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
			else:
				neg += 1

			f.write(str(clf)+'\n')

	return neg,pos,neu,neg+pos+neu