from sklearn.neighbors import KNeighborsClassifier as knn
import pandas as pd

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
