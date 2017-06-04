import PythonApplication1 as main

def train_simple(neu,pos,neg):
	print("---training simple")

	NEUTRALS = set(main.loadFile(neu))
	POSITIVES = set(main.loadFile(pos))
	NEGATIVES = set(main.loadFile(neg))

	return [NEUTRALS,POSITIVES,NEGATIVES]

def test_simple(model, data):
	print("---testing simple")
	results = []
	time_start = main.getTime()
	for line in data:
		res = single_sample_simple(model, line)
		results.append(res)
	time_end = main.getTime()
	print("Simple time elapsed: " + str(time_end - time_start))
	return results

def single_sample_simple(model, line):
	score = 0

	words = line.split(' ')
	for word in words:
		if word in model[0]:
			score += 1
		elif word in model[1]:
			score -= 1

	return 0 if score < 0 else 1 if score > 0 else 2 