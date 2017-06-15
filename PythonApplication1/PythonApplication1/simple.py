import PythonApplication1 as main
import random as r
import math

def train_simple(neg,pos,neu, percent = 1.0):
	neuWords = main.loadFile(neu)
	posWords = main.loadFile(pos)
	negWords = main.loadFile(neg)
	neusize = len(neuWords) * percent
	possize = len(posWords) * percent
	negsize = len(negWords) * percent
	r.shuffle(neuWords)
	r.shuffle(posWords)
	r.shuffle(negWords)
	NEUTRALS = set(neuWords[:math.ceil(neusize)])
	POSITIVES = set(posWords[:math.ceil(possize)])
	NEGATIVES = set(negWords[:math.ceil(negsize)])
	return [NEGATIVES,POSITIVES,NEUTRALS]

def test_simple(model, data):
	results = []
	time_start = main.getTime()
	for line in data:
		res = single_sample_simple(model, line)
		results.append(res)
	time_end = main.getTime()
	return results

def single_sample_simple(model, line):
	score = 0
	neutral_filter,max = 0,2
	words = line.split(' ')
	for word in words:
		if word in model[2]:
			neutral_filter += 1
		elif word in model[1]:
			score += 1
		elif word in model[0]:
			score -= 1
		if neutral_filter == max:
			return 2	
	return 0 if score < 0 else 1 if score > 0 else 2 