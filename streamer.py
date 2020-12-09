"""
This file used for streaming tweets with tweepy api.
"""

import json
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import preprocess
# import traceback

# Your access credientials
accessToken = '869596203327123456-pAEn8eMGB02PlxlKWSDelaS0bZ9imCE'
secretAccessToken = 'SKt0XS5iJLkSKNJ1Be7DgMJbYsafSqP5PBdk7GfICKidO'

# Consumer key and secret
consumerKey = '3FtbXAbWkvBrHbIjg5Q2xA1rt'
consumerSecret = 'XZV0zQB9CopGfUrl2vHCtUSk30y0kBWzLPG9OWmRgPGSwCSB9s'

# Create a StreamListener class
class MyListener(StreamListener):

    def __init__(self, time_limit=30, file_name='tweets.json', location_filter='michigan'):
        self.start_time = time.time()
        self.limit = time_limit
        self.file_name = file_name
        self.outFile = open(self.file_name, 'a')
        self.counter = 0
        self.tweets_gone = 0
        self.location_filter = location_filter
        super(MyListener, self).__init__()

    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            # json.dump(data, self.outFile)
            # self.outFile.write(data)
            tweet = json.loads(data)

            try:
                # I'm not sure if this will work.
                # not tweet['retweeted'] and
                if 'RT @' not in tweet['text'] and tweet['lang'] == 'en' \
                        and (tweet['user']['location'] and self.location_filter in tweet['user']['location'].lower()):
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


                    new_tweet = preprocess.preprocess_tweet(new_tweet)
                    # Preprocessing as a whole is a little messy and kind of scattered around the whole project.



                    json.dump(new_tweet, self.outFile)
                    self.outFile.write('\n')
                    self.counter += 1
                    print(new_tweet['text'], new_tweet['user']['location'])

                    return True
            except KeyError:
                # traceback.print_exc()
                if 'limit' in data:
                    time.sleep(1)

            self.tweets_gone += 1
            if self.tweets_gone % 1000 == 0:
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

    stream = Stream(auth, MyListener(time_limit=15*60, file_name='data/preprocessed_michigan_tweets.json'))
    keywords = ['corona', 'quarantine', 'covid']
    stream.filter(track=keywords)

    print('Finished')
