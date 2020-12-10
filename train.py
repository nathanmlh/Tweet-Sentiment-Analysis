"""
Train script for training and model and getting predictions from unseen data.
This script splits data in a 2:8 testing and training split.

There are good tutorials for this sort of thing.
https://stackabuse.com/python-for-nlp-sentiment-analysis-with-scikit-learn/
This is a one I managed to get working. However, the accuracy is very low.
"""

import json
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import preprocess
from dateutil.parser import parse

if __name__ == "__main__":
    data = []
    # Getting labeled data
    with open('labeled_data/all_labeled_data.json') as f:
        for line in f:
            data.append(json.loads(line))

    # Getting michigan data
    with open('data/preprocessed_michigan_tweets.json', 'r') as f:
        michigan_tweets_data = [json.loads(line) for line in f]
    michigan_tweets = pd.DataFrame(michigan_tweets_data)
    # Preprocesses features
    mt = michigan_tweets['text']
    michigan_dates = np.array([parse(item).date() for item in michigan_tweets['created_at']])


    dataFrame = pd.DataFrame(data)
    # print(dataFrame.head())

    # Getting features and labels
    # Number of good/bad words.
    # Text array
    ta = dataFrame['text']
    allData = np.concatenate([ta, mt])
    textArray = preprocess.preprocess_features(allData)

    # If we are using positive/negative word feature vector
    # positiveWordFeature = preprocess.getPositiveWordFeature(dataFrame['text'])
    # negativeWordFeature = preprocess.getNegativeWordFeature(dataFrame['text'])
    processed_features = np.array(textArray)
    labels = dataFrame['label']
    # Adding null labels for data

    # Separating data after we have preprocessed it
    split_data = processed_features[:500]
    michigan_test_data = processed_features[500:]


    # Splitting into training and testing data
    # TODO: Try different splits
    # TODO: Try more features?
    X_train, X_test, y_train, y_test = train_test_split(split_data, labels, test_size=0.3, random_state=0)

    # Forest classifier
    text_classifier = RandomForestClassifier(n_estimators=1000, random_state=0)
    text_classifier.fit(X_train, y_train)

    # Predictions
    predictions = text_classifier.predict(X_test)

    # Output metrics about predictions.
    # print('confusion matrix', confusion_matrix(y_test, predictions))
    print('classification report \n', classification_report(y_test, predictions))
    print('accuracy \n', accuracy_score(y_test, predictions))


    # This fails because when we preprocess features on line 62 TfidfVectorizer returns a different shaped array for some reason.
    michigan_predictions = text_classifier.predict(michigan_test_data)

    # Setting predictions
    michigan_tweets['label'] = michigan_predictions
    # for i, prediction in enumerate(michigan_predictions):
    #     michigan_tweets[i]['label'] = prediction

    # Outputting
    # for i, tweet in enumerate(mt):
    #     print('Rating: {}, Date: {}, tweet: {}'.format(michigan_predictions[i], michigan_dates[i], tweet))

    michigan_tweets["created_at"] = michigan_tweets["created_at"].apply(lambda x: parse(x))
    day = michigan_tweets["created_at"].dt.to_period("D")
    agg = michigan_tweets.groupby([day])
    for group in agg:
        tweets_processed = group[1].shape[0]
        net_sentiment = group[1]['label'].sum()
        print('{} tweets processed for {}, Net sentiment: {}'.format(group[1].shape[0], group[0], net_sentiment))







