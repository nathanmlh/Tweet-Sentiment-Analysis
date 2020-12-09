"""
This file is used for general script purposes.
"""

import json


def printTweets(filename):
    data =[]
    with open(filename, 'r') as f:
        # for line in f:
        data = [json.loads(line) for line in f]

    counter = 1
    for tweet in data:
        if tweet['user']['location'] and 'Michigan' in tweet['user']['location']:
            print(tweet['text'], tweet['label'])
            counter += 1
    print('outputted {} tweets'.format(counter))

def filterTweetsOnLocation(filename, resulting_file_name, location):
    """
    Saves the given files tweets into a new file filtering on location.
    :param filename: The filename that has the data
    :param resulting_file_name: The resulting file name
    :param location: String of location
    """
    with open(filename, 'r') as f:
        data = [json.loads(line) for line in f]

    with open(resulting_file_name, 'a') as f:
        for tweet in data:
            if tweet['user']['location'] and location in tweet['user']['location'].lower():
                json.dump(tweet, f)
                f.write('\n')

if __name__ == '__main__':
    # printTweets('data/tweets.json')
    filterTweetsOnLocation('data/tweets.json', 'data/preprocessed_michigan_tweet.json', 'michigan')


