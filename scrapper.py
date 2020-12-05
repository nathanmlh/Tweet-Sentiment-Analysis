import json
import operator


def printTweets(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(json.loads(line))

    counter = 1
    for tweet in data:
        if tweet['user']['location'] and 'Michigan' in tweet['user']['location']:
            print(tweet['text'], tweet['label'])
            counter += 1
    print('outputted {} tweets'.format(counter))

if __name__ == '__main__':
    printTweets('data/tweets.json')


