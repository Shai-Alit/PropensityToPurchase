# -*- coding: utf-8 -*-
"""
Created on Fri May 10 09:40:53 2024

@author: seford
"""
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

WORKSPACE = os.environ['WORKSPACE']

df = pd.read_csv(WORKSPACE + '/data/Google Analytics.csv')

y = df['Ordered']

x = df[['RecencyScore','FrequencyScore','MonetaryScore']]

clf = LogisticRegression(random_state=0).fit(x,y)


preds = clf.predict(x)

probs = clf.predict_proba(x)

pickle.dump(clf, open(WORKSPACE + '/github/PropensityToPurchase/models/logreg.pickle', 'wb'))
print('completed')