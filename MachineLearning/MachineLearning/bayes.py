# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
import main

from collections import Counter

# ---------------------------------------------------------------------
# Naive Bayes Model Methods
# ---------------------------------------------------------------------

# Trains a 1-gram Naive Bayes model
def train_bayes(data):
	negWords = []
	posWords = []
	neuWords = []

	for line,clf in data:
		list = line.split(' ')
		if clf == 2:
			neuWords.extend(list)
		elif clf == 1:
			posWords.extend(list)
		elif clf == 0:
			negWords.extend(list)
		else:
			raise Exception('Classification has a non-accepted label')

	neuSet = Counter(neuWords)
	posSet = Counter(posWords)
	negSet = Counter(negWords)

	allSet = set(negWords+posWords+neuWords)
	count = len(allSet)

	lexicon = dict()
	for word in allSet:
		if word not in neuSet:
			neuSet[word] = 0.0
		if word not in posSet:
			posSet[word] = 0.0
		if word not in negSet:
			negSet[word] = 0.0
		lexicon[word] = [float(negSet[word]) / float(count), float(posSet[word]) / float(count), float(neuSet[word]) / float(count)]

	return lexicon

# Predicts a dataset using a trained 1-gram Naive Bayes model
def test_bayes(model, data):
	results = []
	for line in data:
		res = single_sample_bayes(model, line)
		results.append(res)
	return results

# Predicts a single sample using a trained 1-gram Naive Bayes model
def single_sample_bayes(model, line):
	words = line.split(' ')
	cp = [1/3,1/3,1/3]
	for clf in range(len(cp)):
		for word in words:
			if word in model and model[word][clf] != 0:
				cp[clf] *= model[word][clf]
			else:
				cp[clf] *= 1 / (len(model.keys()) + 1) 

	if cp[0] == cp[1]:
		return 2
	if cp[0] < cp[1]:
		return 1 if cp[1] >= cp[2] else 2
	if cp[1] < cp[0]:
		return 0 if cp[0] >= cp[2] else 2