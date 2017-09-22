#!/usr/bin/env python
import itertools
import pandas as pd
from sklearn import svm
from sklearn.metrics import confusion_matrix
from nn import plot_confusion_matrix

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

# Produce confusion matrix
pred = clf.predict(testData)

# Compute confusion matrix
cnf_matrix = confusion_matrix(testLabel, pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=[3,4,5],
                      title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=[3,4,5], normalize=True,
                      title='Normalized confusion matrix')

plt.show()