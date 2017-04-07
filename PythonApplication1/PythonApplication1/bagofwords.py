import numpy as np
import random as r
from preprocessing import *
import tensorflow as tf
from collections import Counter

'''
BAG OF WORDS - TODO: IMPROVE PREPROCESS
'''

FILE_pos = "ds_pos_p"
FILE_neg = "ds_neg_p"

lexicon = []

def make_Lexicon(allLines):
    upper,lower = 1000000,0 #Optimize this

    retLex = []
    tmpLex = []

    for line in allLines:
        words = line.replace('\n','').split(' ')
        for word in words:
            tmpLex.append(word)

    print(len(tmpLex))

    count = Counter(tmpLex)
    for word in count:
        if upper > count[word] > lower:
            retLex.append(word)

    print(len(retLex))

    return retLex

def make_singleSample(line, lexicon, classification):
    feature = np.zeros(len(lexicon))
    words = line.replace('\n','').split(' ')
    for word in words:
        if word in lexicon:
            index = lexicon.index(word) #O(n)
            feature[index] += 1
    return [feature, classification]

def make_lexicon_and_Samples(testSize=0.1):
    posLines = []
    negLines = []

    with open(getDataPath(FILE_pos), "r") as f:
        for line in f:
            posLines.append(line)
            
    with open(getDataPath(FILE_pos), "r") as f:
        for line in f:
            negLines.append(line)

    global lexicon
    lexicon = make_Lexicon(posLines+negLines)
    #print(lexicon)
    
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

'''
NEURAL NETWORK - TODO: IMPROVE ACCURACY
'''


train_x,train_y,test_x,test_y = make_lexicon_and_Samples()
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