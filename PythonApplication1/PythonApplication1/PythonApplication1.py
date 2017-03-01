#import tensorflow as tf
from TwitterAPI import TwitterAPI

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
    r = api.request('statuses/filter', {'track':'pizza'})
    for item in r.get_iterator():
        if 'text' in item:
            print(item['text'].encode('utf-8'))

if __name__ == '__main__':
    test()