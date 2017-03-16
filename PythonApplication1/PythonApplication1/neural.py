import tensorflow as tf

FILE = "2017Mar08"
NUM_CLASSES = 3
NUM_WORDS = 30

def neural():
    print("Semantics analysis for " + FILE + " . . .")



def setup():
    with tf.name_scope('semantics'):
        x = tf.placeholder(tf.string, [None, NUM_WORDS])
        W = tf.Variable(tf.zeros([NUM_WORDS, NUM_CLASSES]))
        b = tf.Variable(tf.zeros([NUM_CLASSES]))
        y = tf.matmul(x, W) + b

        y_
