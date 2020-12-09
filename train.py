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

if __name__ == "__main__":
    data = []
    with open('labeled_data/all_labeled_data.json') as f:
        for line in f:
            data.append(json.loads(line))


    dataFrame = pd.DataFrame(data)
    print(dataFrame.head())

    # Getting features and labels
    # Number of good/bad words.
    # Text array
    textArray = preprocess.preprocess_features(dataFrame['text'])

    # If we are using positive/negative word feature vector
    # positiveWordFeature = preprocess.getPositiveWordFeature(dataFrame['text'])
    # negativeWordFeature = preprocess.getNegativeWordFeature(dataFrame['text'])
    processed_features = np.array(textArray)
    labels = dataFrame['label']

    # Splitting into training and testing data
    # TODO: Try different splits
    # TODO: Try more features?
    X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.3, random_state=0)

    # Forest classifier
    text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
    text_classifier.fit(X_train, y_train)

    # Predictions
    predictions = text_classifier.predict(X_test)

    # Output metrics about predictions.
    print('confusion matrix', confusion_matrix(y_test, predictions))
    print('classification report', classification_report(y_test, predictions))
    print('accuracy', accuracy_score(y_test, predictions))

    # Getting michigan data
    with open('data/preprocessed_michigan_tweets.json', 'r') as f:
        michigan_tweets_data = [json.loads(line) for line in f]

    michigan_tweets = pd.DataFrame(michigan_tweets_data)
    # Preprocesses features
    michigan_text_array = preprocess.preprocess_features(michigan_tweets['text'])
    processed_michigan_features = np.array(michigan_text_array)

    # This fails because when we preprocess features on line 62 TfidfVectorizer returns a different shaped array for some reason.
    # michigan_predictions = text_classifier.predict(michigan_text_array)

    # Outputting
    # for i, tweet in enumerate(michigan_tweets):
    #     print('Rating: {}, tweet: {}'.format(michigan_predictions, tweet))






