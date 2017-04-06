import numpy as np
import tensorflow as tf
import nltk
from nltk import *

FILE = "2017Mar08"
NUM_CLASSES = 2
BATCH_SIZE = 100

train_x, train_y = [],[]
test_x, test_y = [],[]

n_hl1 = 500
n_hl2 = 500
n_hl3 = 500

x = tf.placeholder('float', [None, len(train_x)])
y = tf.placeholder('float')


def neural(data):
    print("Semantics analysis for " + FILE + " . . .")

    hl1 = {'weights': tf.Variable(tf.random_normal([len(train_x[0]), n_hl1]))
          ,'biases' : tf.Variable(tf.random_normal([n_hl1])) }

    hl2 = {'weights': tf.Variable(tf.random_normal([n_hl1, n_hl2]))
          ,'biases' : tf.Variable(tf.random_normal([n_hl2])) }

    hl3 = {'weights': tf.Variable(tf.random_normal([n_hl2, n_hl3]))
          ,'biases' : tf.Variable(tf.random_normal([n_hl3])) }

    out = {'weights': tf.Variable(tf.random_normal([n_hl3, NUM_CLASSES]))
          ,'biases' : tf.Variable(tf.random_normal([NUM_CLASSES])) }

    l1 = tf.add(tf.matmul(data, hl1['weights']), hl1['biases'])
    l1 = tf.nn.relu(l1)

    l2 = tf.add(tf.matmul(l1, hl2['weights']), hl2['biases'])
    l2 = tf.nn.relu(l2)

    l3 = tf.add(tf.matmul(l2, hl3['weights']), hl3['biases'])
    l3 = tf.nn.relu(l3)

    return tf.matmul(l3, out['weights']) + out['biases']
    

def train(x):
    prediction = neural(x)
    cost = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(prediction))
    optimizer = tf.train.AdamOptimizer().minimize(cost)

    hm_epochs = 10

    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for i in range(int(mnist.train.num_examples/BATCH_SIZE)):
                print("TBD")


def setup():
    with tf.name_scope('semantics'):
        print()
