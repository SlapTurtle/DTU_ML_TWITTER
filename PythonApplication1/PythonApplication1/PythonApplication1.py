#import tensorflow as tf
from TwitterAPI import TwitterAPI
import datetime
import os

SEARCHTAG_PATH = 'Files\searchtags.txt'

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


def test():
    consumer_key = 'o5aaDQNePqeOwLJpXFC1qeWmL'
    consumer_secret = 'TM8g6A7GveM5wkZahV8ZgILYGHJcChVNVJblAEn6ZdL9gLCVnA'
    access_token_key = '3688759636-pYAsFBCIAFphzdwvNZjrbcydWFLZ2NFogRybaGc'
    access_token_secret = 'hmM8DZAnLMGn7lGrGbU697eIB0hwbK8XheUXSIQM5CruM'
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    '''r = api.request('search/tweets', {'q':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print(item['text'].encode('utf-8'))
        elif 'message' in item:
            print('{} ({})'.format(item['message'], item['code']))
    '''
    r = api.request('statuses/filter', {'track':{*getSearchTags()}})
    for item in r.get_iterator():
        '''if 'created_at' in item:
            print(item['created_at'])            
            print(datetime.datetime.now())'''
        if 'text' in item:
            print(item['text'].encode('utf-8'))

if __name__ == '__main__':
    test()