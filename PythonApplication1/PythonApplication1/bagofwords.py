import numpy as np
import random as r
from preprocessing import *
import tensorflow as tf
from collections import Counter

'''
BAG OF WORD - TODO: IMPROVE PREPROCESS
'''

FILE = "SentimentAnalysisDataset"
DATA_PATH = 'Files\\'

lexicon = []

def make_Lexicon(allLines):
    global lexicon
    upper,lower = 1000,50 #Optimize this

    retLex = []
    tmpLex = []

    for line in allLines:
        words = line.replace('\n','').split(' ')
        for word in words:
            tmpLex.append(word)
    count = Counter(tmpLex)
    for word in count:
        if upper > count[word] > lower:
            retLex.append(word)

    lexicon = retLex
    return lexicon

def make_singleSample(line, lexicon, classification):
    feature = np.zeros(len(lexicon))
    words = line.replace('\n','').split(' ')
    for word in words:
        if word in lexicon:
            index = lexicon.index(word) #O(n)
            feature[index] += 1
    return [feature, classification]

def make_lexicon_and_Samples(posLines,negLines,testSize=0.1):
    global lexicon
    make_Lexicon(posLines+negLines)

    print(lexicon)
    
    features = []
    for line in posLines:
        features.append(make_singleSample(line, lexicon, [1,0]))
    for line in negLines:
        features.append(make_singleSample(line, lexicon, [0,1]))
    
    r.shuffle(features)
    features = np.array(features)

    testingSize = int(testSize*len(features))

    train_x = list(features[:,0][:-testingSize])
    train_y = list(features[:,1][:-testingSize])
    
    test_x = list(features[:,0][-testingSize:])
    test_y = list(features[:,1][-testingSize:])

    return train_x,train_y,test_x,test_y

def testLex(file=FILE):
    posLines = []
    negLines = []

    with open(file, "r") as f:
        k,max = 0,10000
        for line in f:
            line = str(line).replace('\n','')

            i,j = 0,0
            pos = None
            while(j<3):
                if(line[i] == ','):
                    j += 1
                    if(j == 1):
                        pos = (line[i+1] == '1')                 
                i += 1
            if pos:
                posLines.append(line[i:])
            else:                
                negLines.append(line[i:])

            k += 1
            if k > max : break

    return make_lexicon_and_Samples(posLines,negLines)

'''
NEURAL NETWORK - TODO: IMPROVE ACCURACY
'''

train_x,train_y,test_x,test_y = testLex()
size = len(train_x[0])

n_nodes_hl1 = 500
n_nodes_hl2 = 500
n_nodes_hl3 = 500

n_classes = 2
batch_size = 100

x = tf.placeholder('float', [None, size])
y = tf.placeholder('float')

def neural_network_model(data):
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

def train_neural_network(data=x):
    prediction = neural_network_model(data)

    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(logits=prediction, labels=y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    hm_epochs = 10
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

            print('Epoch', epoch+1, 'completed out of',hm_epochs,'loss:',epoch_loss)

        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:test_x, y:test_y}))