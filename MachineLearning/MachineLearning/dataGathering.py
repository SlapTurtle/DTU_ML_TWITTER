# ---------------------------------------------------------------------
# Imports
# ---------------------------------------------------------------------
import main

from threading import Thread
from time import sleep

# Twitter API
from TwitterAPI import *
# documentation:	https://github.com/geduldig/TwitterAPI/blob/master/docs/
# status codes:		https://dev.twitter.com/streaming/overview/connecting

# ---------------------------------------------------------------------
# Twitter Authentication Keys
# ---------------------------------------------------------------------
consumer_key = 'o5aaDQNePqeOwLJpXFC1qeWmL'
consumer_secret = 'TM8g6A7GveM5wkZahV8ZgILYGHJcChVNVJblAEn6ZdL9gLCVnA'
access_token_key = '3688759636-pYAsFBCIAFphzdwvNZjrbcydWFLZ2NFogRybaGc'
access_token_secret = 'hmM8DZAnLMGn7lGrGbU697eIB0hwbK8XheUXSIQM5CruM'


# ---------------------------------------------------------------------
# Data Gathering Methods
# ---------------------------------------------------------------------

api = None
HB = "------------------------------"

# Reads seachtags from file
def getSearchTags():
    tags = main.loadFile(main.FILE_tag)
    return set(tags)

# Transforms the date to s string
def translateDate(s):
    return s[-4:]+s[4:7]+s[8:10] #fixed string index's

# Connects to twitter and starts collecting data
# Automatically reconnects when disconnected.
def readData(exitTread):
    global api
    api = TwitterAPI(consumer_key, consumer_secret, access_token_key, access_token_secret)
    searchTags = getSearchTags()
    
    print(HB)
    print("Searchtags are:")
    print(searchTags)
    print(HB)

    timerCount = 1
    while (exitTread.isAlive()):
        try:
            r = api.request('statuses/filter', {'track':searchTags, 'language':{'en'}})
            iterator = r.get_iterator()
            printStatus(r.status_code)
            for item in iterator:
                if 'created_at' and 'text' in item:
                    timerCount = 1
                    path = main.getDataPath(main.RAW_PATH + translateDate(item['created_at']))
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
                        wait(timerCount, r)
                        timerCount *= 2
                        break
                if not exitTread.isAlive():
                    # program ended by user
                    break
        except ValueError:
            # something needs to be fixed before re-connecting
            raise 
        except TwitterRequestError as e:
            if e.status_code == 420 or e.status_code == 503:
                # temporary interruption, re-try request
                wait(timerCount, r)
                timerCount *= 2
                pass
            else:
                raise                
        except TwitterConnectionError:
            # temporary interruption, re-try request
            wait(timerCount, r)
            timerCount *= 2
            pass
        except:
            # temporary interruption, re-try request
            wait(timerCount, r)
            timerCount *= 2
            pass

    print(HB)
    print("Stopping data retrieval...")
    print(HB)

# sleeps a set amount of time
def wait(timerCount, r):
    print(HB)
    print("Disconnected, attempting to reconnect in {} seconds...".format(str(timerCount*60 + 5)))
    print(HB)
    r.close()
    sleep(timerCount*60 + 5)

# prints status information when attempting to reconnect
def printStatus(s):
    stat = (str(s) + " - good!") if (s == 200) else (str(s) + " - bad!")
    print("Status is: {}".format(stat))
    print(HB)
    if stat == 200:
        print("Downloading Tweets...")
        print(HB)

# Ends exitthread by input
def getInput():
    input()

# Starts the data gathering
def startData():
    t = Thread(target = getInput)
    t2 = Thread(target = readData, args={t})
    t.start()
    t2.start()
    t.join()
    t2.join()