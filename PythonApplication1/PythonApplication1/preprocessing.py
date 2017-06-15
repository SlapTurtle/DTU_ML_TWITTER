import PythonApplication1 as main
import re
import nltk

from string import digits
from time import time

FILE = "2017May04"

POSITIVES = set()
NEGATIVES = set()
NOISE = set()
TAGS = set()

def parseSet(file = "SentimentAnalysisDataset"):
	global POSITIVES, NEGATIVES, NOISE, TAGS

	NOISE = set(["rt", "n", "i", "u", "it", "its", "us", "we", "you", "me", "they", "your", "my", "on", "of", "in", "by", "at", "to", "from", "for", "a", "an", "im", "r", "this", "those", "that", "them", "the"])
	TAGS = getTags()

	time_start = time()

	POSITIVES = set(main.loadFile("positives"))
	NEGATIVES = set(main.loadFile("negatives"))

	clearfile("ds_pos")
	clearfile("ds_neg")
	time_start = time()
	print("Parsing set . . .")
	with open(main.getDataPath(file), "r", encoding='utf8') as f:
		k = 0
		for line in f:
			line = str(line.encode('utf-8')).replace('\n','')
			i,j = 0,0
			pos = None
			while(j<3):
				if(line[i] == ','):
					j += 1
					if(j == 1):
						pos = (line[i+1] == '1')                 
				i += 1

			ds = "ds_pos_p" if pos else "ds_neg_p"
			with open(main.getDataPath(ds), "a") as fi:
				res = prep(line[i:])[:-2]
				if res != []:
					fi.write(str(res) + "\n")
			k += 1

			if k % 1000 == 0:
				print("Finished " + str(k))
	time_end = time()
	print("Processed " + file + " in " + (str)(time_end - time_start)[:4] + "s")


def processMar():
	for date in range(17,32):
		try:
			process("2017Mar" + str(date))
		except:
			print("Date " + str(date) + " not found")
			pass


def processMay():
	for date in range(21,32):
		try:
			zero = "0" if date < 10 else ""
			process("2017May" + zero + str(date))
		except:
			print("Date " + str(date) + " not found")
			pass

def processDataSet():
	for h in ["hneg", "hpos", "hneu"]:
		process(h)

def process(file = FILE):
	global POSITIVES, NEGATIVES, NOISE, TAGS

	NOISE = set(["rt", "n", "i", "u", "it", "its", "us", "we", "you", "me", "they", "your", "my", "on", "of", "in", "by", "at", "to", "from", "for", "a", "an", "im", "r", "this", "those", "that", "them", "the"])
	TAGS = getTags()

	time_start = time()
	data = open(main.getDataPath(main.RAW_PATH + file))
	clearfile(main.PRE_PATH + file)

	recent = [""] * 40
	index = 0

	POSITIVES = set(main.loadFile("positives"))
	NEGATIVES = set(main.loadFile("negatives"))

	linecount = 0
	removed = 0

	for line in data:
		linecount += 1
		#text = get_text(line)
		text = line
		result = prep(text)
		if (result == []):
			removed += 1
			continue
		spam = False
		for r in recent:
			if result == r:
				#spam = True
				break
		if not spam:
			filedump(result + "\n", file)
			recent[index] = result
			if (1 + index < len(recent)):
				index = index + 1
			else:
				index = 0

	time_end = time()
	print("Processed " + file + " in " + (str)(time_end - time_start)[:4] + "s")
	print(str(removed) + " of " + str(linecount) + " lines filtered out\n")


# get text from data string
def get_text(string):
	string = string.replace('\"', "'", 1)
	date, text = string.split("'", 1)
	return text[:-1]

# prep
def prep(string):
	tokenized = tokenize(re.sub('[\']', '', string))
	if (tokenized == []):
		return []
	prol = alter_prolonged(tokenized)
	result = ""
	for t in prol:
		result = result + t + " "
	return result[:-1]


# cool stuff
def tokenize(string):
	list = re.split("\W+|_", string)
	tokenized = [x.lower() for x in list]
	#tokenized = filter(tokenized)
	if (tokenized == []):
		return []
	i = 0
	while(i != len(tokenized)):
		no_digits = str.maketrans('', '', digits)
		tokenized[i] = tokenized[i].translate(no_digits)
		word = tokenized[i]

		if (word == "https" or word == "nhttps"):
			try:
				for j in range(0,4):
					tokenized.pop(i)
			except:
				pass
		elif (i > 0 and (word == "t" or word == "nt" or word == "re" or word == "s")):
			tokenized[i-1] = tokenized[i-1] + word
			tokenized.pop(i)
		elif (len(word) < 1) or (len(word) <= 3 and word[0] == 'x') or (word in NOISE):
			tokenized.pop(i)
		else:
			i = i + 1
	return tokenized


# alteration of prolonged words + stemming
def alter_prolonged(list = []):
	stemmer = nltk.stem.porter.PorterStemmer()
	res = list.copy()
	for v in range(len(list)):
		i = 0
		j = -1
		w = list[v]
		while(i + 2 < len(w)):
			if (w[i] == w[i+1] and w[i+1] == w[i+2]):
				w = w[:i] + w[(i+1):]
				j = i
			else:
				i+= 1
		if (not (w in POSITIVES or w in NEGATIVES)) and j != -1:
			w = w[:j] + w[(j+1):]
		try:
			res[v] = stemmer.stem(w)
		except:
			print("Could not stem word '" + w + "'")
			res[v] = w
			pass
	return res

#filter
def filter(list):
	for word in list:
		if (word in TAGS):
			return list
	return []

def getTags():
	path = main.getDataPath(main.FILE_tag + "_f")
	tags = set()
	with open(path, "r") as file:
		for line in file:
			tags.add(line[:-1])
	return tags

# clear file before writing
def clearfile(file = FILE):
	dp = main.getDataPath(file)[:-4] + "_p.txt"
	with open(dp, "w") as f:
		f.write("")

# write to _p file
def filedump(s, file = FILE):
	dp = main.getDataPath(main.PRE_PATH + file)[:-4] + "_p.txt"
	with open(dp, "a") as file:
		file.write(s)