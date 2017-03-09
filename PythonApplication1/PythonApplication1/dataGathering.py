import PythonApplication1 as main
from TwitterAPI import *
from threading import Thread

consumer_key = 'o5aaDQNePqeOwLJpXFC1qeWmL'
consumer_secret = 'TM8g6A7GveM5wkZahV8ZgILYGHJcChVNVJblAEn6ZdL9gLCVnA'
access_token_key = '3688759636-pYAsFBCIAFphzdwvNZjrbcydWFLZ2NFogRybaGc'
access_token_secret = 'hmM8DZAnLMGn7lGrGbU697eIB0hwbK8XheUXSIQM5CruM'

SEARCHTAG_PATH = 'searchtags'

HB = "------------------------------"

def getSearchTags():
    path = main.getDataPath(SEARCHTAG_PATH)
    tags = set()
    with open(path, "r") as file:
        for line in file:
            tags.add(line[:-1])
    return tags

def translateDate(s):
    return s[-4:]+s[4:7]+s[8:10] #fixed string index's

def readData(t):
    ''' Code assistance: https://github.com/geduldig/TwitterAPI/blob/master/docs/ '''
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    searchTags = getSearchTags()
    
    print(HB)
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
                    path = main.getDataPath(translateDate(item['created_at']))
                    s = '[{}] {}\n'.format(item['created_at'], item['text'].encode('utf-8'))
                    with open(path, "a") as file:
                        file.write(s)
                    #print(s[:-1])
                elif 'disconnect' in item:
                    print(HB)
                    print('Disconnected because {}'.format(item['disconnect']['reason']))
                    event = item['disconnect']
                    if event['code'] in [2,5,6,7]:
                        # something needs to be fixed before re-connecting
                        raise ValueError('Stop Reconnect!',event['reason'])
                    else:
                        # temporary interruption, re-try request
                        wait(timerCount)
                        timerCount *= 2
                        break
                if not t.isAlive():
                    # program ended by user
                    break
        except ValueError:
            # something needs to be fixed before re-connecting
            raise 
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
        except:
            # temporary interruption, re-try request
            wait(timerCount)
            timerCount *= 2
            pass

    print(HB)
    print("Stopping data retrieval...")
    print(HB)

def wait(timerCount):
    print(HB)
    print("Disconnected, attempting to reconnect in {} seconds...".format(str(timerCount*60)))
    time.sleep(timerCount*60)

def printStatus(s):
    stat = (str(s) + " - good!") if (s == 200) else str(s)
    print(HB)
    print("Status is: {}".format(stat))
    print(HB)
    print("Downloading Tweets...")
    print(HB)

def getInput():
    input()

def startData():
    t = Thread(target = getInput)
    t2 = Thread(target = readData, args={t})
    t.start()
    t2.start()
    t.join()
    t2.join()