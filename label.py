"""
Script to automate labeling of the tweets
"""

import json

YOUR_FILE_NAME = "nathan.json"

if __name__ == '__main__':

    # open file and load data
    data = []
    with open(YOUR_FILE_NAME) as f:
        for line in f:
            data.append(json.loads(line))

    new_file_name = 'labels_' + YOUR_FILE_NAME
    print('new file name:', new_file_name)

    with open(new_file_name, 'a') as out_file:

        # Looping through tweets in data
        for i, tweet in enumerate(data):
            print(tweet['text'])
            label = int(input('[{}] Label for this tweet: '.format(i)))
            tweet['label'] = label

            json.dump(tweet, out_file)
            out_file.write('\n')

