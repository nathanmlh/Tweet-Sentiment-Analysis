import json
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from collections import defaultdict
import operator

# Your access credientials
accessToken = 'your access token'
secretAccessToken = 'your secret access token'

# Consumer key and secret
consumerKey = 'your consumer key'
consumerSecret = 'your consumer secret'

# Create a StreamListener class
class MyListener(StreamListener):

    def __init__(self, time_limit=30, file_name='tweets.json'):
        self.start_time = time.time()
        self.limit = time_limit
        self.file_name = file_name
        self.outFile = open(self.file_name, 'a')
        self.counter = 0
        self.tweets_gone = 0
        super(MyListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            # json.dump(data, self.outFile)
            # self.outFile.write(data)
            tweet = json.loads(data)

            try:
                if not tweet['retweeted'] and 'RT @' not in tweet['text'] and tweet['lang'] == 'en':
                    if 'extended_tweet' in tweet:
                        new_tweet = {'created_at': tweet['created_at'], 'id': tweet['id'], 'text': tweet['extended_tweet']['full_text'],
                                     'url': 'https://twitter.com/twitter/statuses/' + str(tweet['id']),
                                     'user': {'name': tweet['user']['name'],
                                              'screen_name': tweet['user']['screen_name'],
                                              'location': tweet['user']['location']}, 'label': None}
                    else:
                        new_tweet = {'created_at': tweet['created_at'], 'id': tweet['id'], 'text': tweet['text'],
                                 'url': 'https://twitter.com/twitter/statuses/' + str(tweet['id']),
                                 'user': {'name': tweet['user']['name'],
                                          'screen_name': tweet['user']['screen_name'],
                                  'location': tweet['user']['location']}, 'label': None}
                    # print('[{}]: {}'.format(self.counter, new_tweet))
                    self.counter += 1
                    json.dump(new_tweet, self.outFile)
                    self.outFile.write('\n')
                    return True
            except KeyError:
                print('excepted keyerror')
                print(tweet)

            self.tweets_gone += 1
            if self.tweets_gone % 100 == 0:
                print('{} tweets filtered'.format(self.tweets_gone))

        else:
            self.outFile.close()
            return False

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    auth = OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, secretAccessToken)
    print('set auth and access')

    stream = Stream(auth, MyListener(time_limit=300, file_name='data/tweets2.json'))
    # keywords = ['coronavirus',  'covid', 'covid-19', 'mask', 'quarantine',  'corona']
    keywords1 = ['coronavirus', 'covid']
    keywords2 = ['covid-19', 'mask']
    keywords3 = ['quarantine', 'corona']

    # locations = [87.00001, 42.000001, 82.00001, 46.00001]
    #for i in range(10):
    stream.filter(track=keywords1)
    print('filtered on keywords1')
    stream.filter(track=keywords2)
    print('filtered on keywords2')
    stream.filter(track=keywords3)
    print('filtered on keywords3')
    print('sleeping for two minutes.')
        # time.sleep(2 * 60)

    # locations = ['Michigan', 'Michigan, USA']

    print('Finished')
