import tensorflow as tf
import numpy as np
from collections import Counter
import PythonApplication1 as main

def make_Lexicon(allLines):
	#upper,lower = 1000,50 #Optimize this
	upper,lower = 50,2

	retLex = dict()
	tmpLex = []

	for line in allLines:
		words = line.replace('\n','').split(' ')
		for word in words:
			tmpLex.append(word)
	
	count = Counter(tmpLex)
	#print(str(count))
	i = 0
	for word in count:
		if upper > count[word] > lower:
			retLex[word] = i
			i += 1

	#print(str(retLex))

	return retLex

def singleFeature(line, lexicon, classification):
	feature = np.zeros(len(lexicon))
	words = line.split(' ')
	for word in words:
		if word in lexicon:
			index = lexicon[word]
			feature[index] += 1
	return [feature, classification]

def makeFeatures(data, lexicon):
	features = []
	for line,clf in data:
		type = [1,0,0] if clf==0 else [0,1,0] if clf==1  else [0,0,1]
		features.append(singleFeature(line, lexicon, type))
	return features

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 3
batch_size = 50

def neural_network_model(data, size):
	hidden_1_layer = {'weights':tf.Variable(tf.random_normal([size, n_nodes_hl1])),
					  'biases':tf.Variable(tf.random_normal([n_nodes_hl1]))}

	hidden_2_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl1, n_nodes_hl2])),
					  'biases':tf.Variable(tf.random_normal([n_nodes_hl2]))}

	hidden_3_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl2, n_nodes_hl3])),
					  'biases':tf.Variable(tf.random_normal([n_nodes_hl3]))}

	output_layer = {'weights':tf.Variable(tf.random_normal([n_nodes_hl3, n_classes])),
					'biases':tf.Variable(tf.random_normal([n_classes])),}


	l1 = tf.add(tf.matmul(data,hidden_1_layer['weights']), hidden_1_layer['biases'])
	l1 = tf.nn.relu(l1)

	l2 = tf.add(tf.matmul(l1,hidden_2_layer['weights']), hidden_2_layer['biases'])
	l2 = tf.nn.relu(l2)

	l3 = tf.add(tf.matmul(l2,hidden_3_layer['weights']), hidden_3_layer['biases'])
	l3 = tf.nn.relu(l3)

	output = tf.matmul(l3,output_layer['weights']) + output_layer['biases']

	return output

def train_neural_network(train, test, epochCount):
	allLines = [row[0] for row in train]
	lexicon = make_Lexicon(allLines)

	train_features = makeFeatures(train, lexicon)
	test_features = makeFeatures(test, lexicon)

	train_x = [row[0] for row in train_features]
	train_y = [row[1] for row in train_features]
	
	test_x = [row[0] for row in test_features]
	test_y = [row[1] for row in test_features]
	size = len(lexicon)

	x = tf.placeholder('float', [None, size])
	y = tf.placeholder('float')

	prediction = neural_network_model(x,size)

	cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
	optimizer = tf.train.AdamOptimizer().minimize(cost)

	hm_epochs = epochCount
	percent = 0
	with tf.Session() as sess:
		sess.run(tf.global_variables_initializer())

		for epoch in range(hm_epochs):
			epoch_loss = 0
			i = 0
			while(i < len(train_x)):
				start,end = i,i+batch_size
				batch_x = np.array(train_x[start:end])
				batch_y = np.array(train_y[start:end])

				_, c = sess.run([optimizer, cost], feed_dict={x: batch_x, y: batch_y})
				epoch_loss += c

				i += batch_size

			#print('Epoch', epoch+1, 'completed out of',hm_epochs,'loss:',epoch_loss)

		correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

		time_start = main.getTime()
		accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
		percent = accuracy.eval({x:test_x, y:test_y})
		time_end = main.getTime()
		#print("Neural time elapsed: " + str(time_end - time_start))
	return percent