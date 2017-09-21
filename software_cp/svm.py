#!/usr/bin/env python

import pandas as pd
from sklearn import svm

# Load training and testing dataset
train = pd.read_csv('ds_train.csv')
test = pd.read_csv('ds_test.csv')

trainData  = train.drop('label' , axis=1).drop('part', axis=1).values
trainLabel = train.label.values

testData  = test.drop('label' , axis=1).drop('part', axis=1).values
testLabel = test.label.values

# train SVM SVC

clf = svm.SVC(decision_function_shape='ovo')
clf.fit(trainData , trainLabel)

print("Training set score for SVC : %f" % clf.score(trainData, trainLabel))
print("Test set score for SVC : %f"     % clf.score(testData , testLabel ))