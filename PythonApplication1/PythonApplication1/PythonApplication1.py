#import tensorflow as tf
from TwitterAPI import TwitterAPI
import datetime
import os
from threading import Thread

#kmmen
consumer_key = 'o5aaDQNePqeOwLJpXFC1qeWmL'
consumer_secret = 'TM8g6A7GveM5wkZahV8ZgILYGHJcChVNVJblAEn6ZdL9gLCVnA'
access_token_key = '3688759636-pYAsFBCIAFphzdwvNZjrbcydWFLZ2NFogRybaGc'
access_token_secret = 'hmM8DZAnLMGn7lGrGbU697eIB0hwbK8XheUXSIQM5CruM'

DATA_PATH = 'Files\\'
SEARCHTAG_PATH = 'searchtags.txt'

def directorySkip(s=DATA_PATH):
    path = os.path.dirname(os.path.abspath(__file__))
    if type(path) == str:
        i,j = len(path),0
        while (j!=2):
            i = i-1
            if path[i] == '\\':
                j = j + 1
        return path[0:i+1] + s
    return None

def getSearchTags():
    return directorySkip() + SEARCHTAG_PATH

def getDataPath(s):
    path = directorySkip() + s[-4:]+s[4:7]+s[8:10]+'.txt' #fixed string index's
    open('myfile.dat', 'w+').close()
    return path

def readData(t):
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    path = ''
    searchTags = getSearchTags()
    print(searchTags)
    r = api.request('statuses/filter', {'track':searchTags, 'language':{'en'}})

    for item in r.get_iterator():
        if 'created_at' and 'text' in item:
            path = getDataPath(item['created_at'])
            s = '[{}] {}\n'.format(item['created_at'], item['text'].encode('utf-8'))
            with open(path, "a") as file:
                file.write(s)
        else:
            print(item)
        if(not t.isAlive()):
            break
    print("stopping data")

def getInput():
    print("start")
    input()

if __name__ == '__main__':
    t = Thread(target = getInput)
    t2 = Thread(target = readData, args={t})
    t.start()
    t2.start()
    t.join()
    t2.join()