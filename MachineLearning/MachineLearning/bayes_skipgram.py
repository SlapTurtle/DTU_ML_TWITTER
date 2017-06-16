# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
import main

from collections import Counter

# ---------------------------------------------------------------------
# Naive Bayes Model Methods
# ---------------------------------------------------------------------

# Transform a set of words into a k-skip-n-gram set
def tranform_skipgram(words, skip, gram):
	list = []
	for set in recursive_skipgram(words, skip, gram):
		t = ""
		for s in set:
			t += s
		list.append(t)
	return list 

# Transform a single sentence into a k-skip-n-gram set
# Note that this method is not perfomance optimised
def recursive_skipgram(words, skip, gram):
	allsets = []
	if gram > 0:
		for i in range(len(words)):
			j = i+skip+gram-1
			if j < len(words) or gram == 1:
				if gram == 1:
					allsets.append([words[i]])
				elif gram == 2:
					allsets.append([words[i], words[j]])
					allsets.append([words[j], words[i]])
				elif gram >= 3:
					sets = recursive_skipgram(words[i+1:j], skip, gram-2)
					for subset in sets:
						nw = [words[i]] + subset + [words[j]]
						re = [words[j]] + subset + [words[i]]
						if len(nw) == gram:
							allsets.append(nw)
							allsets.append(re)
	if skip > 0 and gram != 1:
		allsets += recursive_skipgram(words, skip-1, gram)
	return allsets 	

# Trains a k-skip-n-gram Naive Bayes model
def train_bayes_skipgram(data, skip, gram):
	negWords = []
	posWords = []
	neuWords = []

	for line,clf in data:
		list = tranform_skipgram(line.split(' '), skip, gram)
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
def test_bayes_skipgram(model, data, skip, gram):
	results = []
	for line in data:
		res = single_sample_bayes_skipgram(model, line, skip, gram)
		results.append(res)
	return results

# Predicts a single sample using a trained 1-gram Naive Bayes model
def single_sample_bayes_skipgram(model, line, skip, gram):
	words = tranform_skipgram(line.split(' '), skip, gram)
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