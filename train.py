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
from preprocess import preprocess_features

if __name__ == "__main__":
    data = []
    with open('labeled_data/all_labeled_data.json') as f:
        for line in f:
            data.append(json.loads(line))


    dataFrame = pd.DataFrame(data)
    print(dataFrame.head())

    # Getting features and labels
    processed_features = np.array(preprocess_features(dataFrame['text']))
    labels = dataFrame['label']

    # Converting labels to positive / neutral / negative values
    for i, item in enumerate(labels):
        if item == -1:
            labels[i] = 'negative'
        elif item == 0:
            labels[i] = 'neutral'
        else:
            labels[i] = 'positive'

    # Splitting into training and testing data
    X_train, X_test, y_train, y_test = train_test_split(processed_features, labels, test_size=0.2, random_state=0)

    # Forest classifier
    text_classifier = RandomForestClassifier(n_estimators=200, random_state=0)
    text_classifier.fit(X_train, y_train)

    # Predictions
    predictions = text_classifier.predict(X_test)

    # Output metrics about predictions.
    print(confusion_matrix(y_test, predictions))
    print(classification_report(y_test, predictions))
    print(accuracy_score(y_test, predictions))



