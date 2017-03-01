#import tensorflow as tf
from TwitterAPI import TwitterAPI
import datetime
import os

consumer_key = 'o5aaDQNePqeOwLJpXFC1qeWmL'
consumer_secret = 'TM8g6A7GveM5wkZahV8ZgILYGHJcChVNVJblAEn6ZdL9gLCVnA'
access_token_key = '3688759636-pYAsFBCIAFphzdwvNZjrbcydWFLZ2NFogRybaGc'
access_token_secret = 'hmM8DZAnLMGn7lGrGbU697eIB0hwbK8XheUXSIQM5CruM'

SEARCHTAG_PATH = 'Files\searchtags.txt'
DATA_PATH = 'Files\data.txt'

def getSearchTags():
    tags = []
    path = os.path.dirname(os.path.abspath(__file__))
    if type(path) == str:
        i,j = len(path),0
        while (j!=2):
            if path[i-1] == '\\':
                j = j + 1
            i = i-1
        path = path[0:i+1] + SEARCHTAG_PATH
        for line in open(path).readlines():
            tags.append(line[:-1])
    return tags


def readData():
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    path = getDataPath()
    searchTags = *getSearchTags()

    r = api.request('statuses/filter', {'track':{searchTags}})

    with open(path, "a") as myfile:
        for item in r.get_iterator():
            if 'created_at' and 'text' in item:
                s = '[{}] {}\n'.format(item['created_at'], item['text'].encode('utf-8'))
                myfile.write(s)
            

def getDataPath():
    path = os.path.dirname(os.path.abspath(__file__))
    if type(path) == str:
        i,j = len(path),0
        while (j!=2):
            if path[i-1] == '\\':
                j = j + 1
            i = i-1
        path = path[0:i+1] + DATA_PATH
    return path

if __name__ == '__main__':
    readData()