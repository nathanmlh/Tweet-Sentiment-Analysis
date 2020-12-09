"""
Nathan Holdom
This file holds preprocessing functions.
"""

import json
import re
import random
import numpy as np
from nltk.stem import PorterStemmer

# TD-IF stuff
from sklearn.feature_extraction.text import TfidfVectorizer

def getPositiveWordFeature(data):
    """
    Processes the data and returns a feature vector of how many positive words there were
    :return: nparray feature vector
    """
    # A list of positive words
    positiveWords = []
    with open('data/opinion-lexicon-English/positive-words.txt', 'r') as f:
        for line in f:
            positiveWords.append(line.strip())

    featureVector = []
    for tweet in data:
        netSentiment = 0
        # Looping through each tweet text
        for word in tweet.split():
            if word in positiveWords:
                netSentiment += 1
        featureVector.append(netSentiment)
    final = np.array(featureVector)
    return final


def getNegativeWordFeature(data):
    """
    Processes the data and returns a feature vector of how many positive words there were
    :return: nparray feature vector
    """
    # A list of positive words
    negativeWords = []
    with open('data/opinion-lexicon-English/negative-words.txt', 'r') as f:
        for line in f:
            negativeWords.append(line.strip())

    featureVector = []
    for tweet in data:
        netSentiment = 0
        # Looping through each tweet text
        for word in tweet.split():
            if word in negativeWords:
                netSentiment += 1
        featureVector.append(netSentiment)
    final = np.array(featureVector)
    return final


def preprocess_features(features):
    """
    This function preprocesess the given feature.
    """
    processed_features = []

    for sentence in range(0, len(features)):
        # Remove all the special characters
        processed_feature = re.sub(r'\W', ' ', str(features[sentence]))

        # remove all single characters
        processed_feature = re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

        # Remove single characters from the start
        processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature)

        # Substituting multiple spaces with single space
        processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

        # Removing prefixed 'b'
        processed_feature = re.sub(r'^b\s+', '', processed_feature)

        # Converting to Lowercase
        processed_feature = processed_feature.lower()

        # Stemming words
        feature = processed_feature.split(' ')
        ps = PorterStemmer()
        stemmed_words = [ps.stem(w) for w in feature]

        processed_features.append(' '.join(stemmed_words))

    vectorizer = TfidfVectorizer(max_features=2500, min_df=7, max_df=0.8)
    processed_features = vectorizer.fit_transform(processed_features).toarray()

    return processed_features


def preprocess(filename, outputFile, filter=None):
    """
    Preprocesses the file given
    :param filename: Json file name
    :return: True, new_preprocessed_file
    """
    # Array of json objects
    data = []
    # Getting data
    with open(filename) as f:
        for line in f:
            data.append(json.loads(line))

    final_data = []
    for i, tweet in enumerate(data):
        # Removing white space
        text = tweet['text'].replace('\n', ' ')
        # Lower the text and splitting into array
        word_arr = text.lower().split(' ')
        # Removing '@'
        word_arr = [word for word in word_arr if '@' not in word and 'http' not in word]
        # Removing https
        final = ' '.join(word_arr)

        # Making sure any covid words are in the list
        covid_terms = ['covid', 'corona', 'quarantine', 'mask']
        # If  any of the words terms we are looking for are in the final text
        if any(word in final for word in covid_terms):
            # Updating tweet text with final
            tweet['text'] = final
            final_data.append(tweet)
            print('{}: {}'.format(i, final))

    # Loading data into new preprocessed file
    with open(outputFile, 'a') as f:
        for tweet in final_data:
            # Applying filter to output data
            if filter:
                if tweet['user']['location'] and filter in tweet['user']['location'].lower():
                    json.dump(tweet, f)
                    f.write('\n')
                else:
                    continue
            else:
                json.dump(tweet, f)
                f.write('\n')

    return True


def output():
    data = []
    with open('data/preprocessed_tweets.json') as f:
        for line in f:
            data.append(json.loads(line))

    # Outputting data to files
    filenames = ['keerthana.json', 'michael.json', 'scott.json', 'andrew.json', 'ben.json', 'nathan.json']
    for file in filenames:
        with open('data/' + file, 'a') as f:
            # 100 samples for each person
            for tweet in random.sample(data, 100):
                json.dump(tweet, f)
                f.write('\n')


def preprocess_tweet(tweet):
    """
    This function fully preprocesses a tweet's textual data.
    :param tweet: A dictionary of tweet informatiton
    :return: A preprocessed tweet
    """
    text = tweet['text'].replace('\n', ' ')
    # Lower the text and splitting into array
    word_arr = text.lower().split(' ')
    # Removing '@'
    word_arr = [word for word in word_arr if '@' not in word and 'http' not in word]
    # Removing https
    final = ' '.join(word_arr)

    tweet['text'] = final
    return tweet


if __name__ == '__main__':
    preprocess('data/tweets.json', 'data/preprocessed_michigan_tweets.json', filter='michigan')

    # If need to send labeling files to other people
    # output()