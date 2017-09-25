from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix
from plot_helper import plot_confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools



train = pd.read_csv('ds_train.csv')
test = pd.read_csv('ds_test.csv')

trainData  = train.drop('label' , axis=1).drop('part', axis=1).values
trainLabel = train.label.values

testData  = test.drop('label' , axis=1).drop('part', axis=1).values
testLabel = test.label.values

knnclf = knn(n_neighbors=20 , n_jobs=2 , weights='distance')

knnModel = knnclf.fit(trainData , trainLabel)

print("Training set score for KNN: %f" % knnModel.score(trainData , trainLabel))
print("Testing  set score for KNN: %f" % knnModel.score(testData  , testLabel ))

y_pred = knnModel.predict(testData)

# Compute confusion matrix
cnf_matrix = confusion_matrix(testLabel, y_pred)
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
