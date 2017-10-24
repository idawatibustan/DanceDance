from sklearn import preprocessing
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix
from plot_helper import plot_confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import itertools
import pickle

def normalise_data(df_in):
    df_normalised = pd.DataFrame(preprocessing.normalize(df_in.values), columns=df_in.columns)
    return df_normalised

df = pd.read_csv('data_ext/full_checked_extracted.csv')

print np.any(pd.isnull(df))

#df_n = normalise_data(df)
#msk = np.random.rand(len(df_n)) < 0.8

msk = np.random.rand(len(df)) < 0.8

train = df[msk]
test = df[~msk]

trainData  = train.drop('label' , axis=1).values
trainLabel = train.label.values

testData  = test.drop('label' , axis=1).values
testLabel = test.label.values

knnclf = knn(n_neighbors=10 , n_jobs=2 , weights='uniform')

knnModel = knnclf.fit(trainData , trainLabel)

#pickle.dump(knnModel, open('first_activities.knn','wb'))

print("Training set score for KNN: %f" % knnModel.score(trainData , trainLabel))
print("Testing  set score for KNN: %f" % knnModel.score(testData  , testLabel ))

y_pred = knnModel.predict(testData)

# Compute confusion matrix
cnf_matrix = confusion_matrix(testLabel, y_pred)
np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=range(0,11),
title='Confusion matrix, without normalization')

# Plot normalized confusion matrix
plt.figure()
plot_confusion_matrix(cnf_matrix, classes=range(0,11), normalize=True,
title='Normalized confusion matrix')

plt.show()
