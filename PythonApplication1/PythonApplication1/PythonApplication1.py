#import tensorflow as tf
from TwitterAPI import TwitterAPI
import datetime
import os
from threading import Thread
import time

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
    path = directorySkip() + SEARCHTAG_PATH
    tags = set()
    with open(path, "r") as file:
        for line in file:
            tags.add(line[:-1])
    return tags

def getDataPath(s):
    path = directorySkip() + s[-4:]+s[4:7]+s[8:10]+'.txt' #fixed string index's
    open('myfile.dat', 'w+').close()
    return path

def readData(t):
    ''' Code assistance: https://github.com/geduldig/TwitterAPI/blob/master/docs/ '''
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    searchTags = getSearchTags()
    
    print("-----------------------")
    print("Searchtags are:")
    print(searchTags)

    timerCount = 1
    while (t.isAlive()):
        try:
            r = api.request('statuses/filter', {'track':searchTags, 'language':{'en'}})
            printStatus(r.status_code)
            for item in r.get_iterator():
                if 'created_at' and 'text' in item:
                    timerCount = 1
                    path = getDataPath(item['created_at'])
                    s = '[{}] {}\n'.format(item['created_at'], item['text'].encode('utf-8'))
                    with open(path, "a") as file:
                        file.write(s)
                    #print(s[:-1])
                elif 'disconnect' in item:
                    print("-----------------------")
                    print('Disconnected because {}'.format(item['disconnect']['reason']))
                    event = item['disconnect']
                    if event['code'] in [2,5,6,7]:
                        # something needs to be fixed before re-connecting
                        raise Exception(event['reason'])
                    else:
                        # temporary interruption, re-try request
                        wait(timerCount)
                        timerCount *= 2
                        break
                if not t.isAlive():
                    # program ended by user
                    break
        except TwitterRequestError as e:
            if e.status_code < 500:
                # something needs to be fixed before re-connecting
                raise
            else:
                # temporary interruption, re-try request
                wait(timerCount)
                timerCount *= 2
                pass
        except TwitterConnectionError:
            # temporary interruption, re-try request
            wait(timerCount)
            timerCount *= 2
            pass

    print("-----------------------")
    print("Stopping data retrieval:")
    print("-----------------------")

def wait(timerCount):
    print("-----------------------")
    print("Disconnected, attempting to reconnect in {} seconds...".format(str(timerCount*60)))
    print("")
    time.sleep(timerCount*60)

def printStatus(s):
    stat = (str(s) + " - good!") if (s == 200) else str(s)
    print("-----------------------")
    print("Status is: {}".format(stat))
    print("-----------------------")
    print("Downloading Tweets...")
    print("-----------------------")

def getInput():
    input()

if __name__ == '__main__':
    t = Thread(target = getInput)
    t2 = Thread(target = readData, args={t})
    t.start()
    t2.start()
    t.join()
    t2.join()