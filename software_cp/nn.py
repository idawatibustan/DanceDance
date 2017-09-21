#!/usr/bin/env python

import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
import sklearn.neural_network as nn

# Load training and testing dataset
train = pd.read_csv('ds_train.csv')
test = pd.read_csv('ds_test.csv')

trainData  = train.drop('label' , axis=1).drop('part', axis=1).values
trainLabel = train.label.values

testData  = test.drop('label' , axis=1).drop('part', axis=1).values
testLabel = test.label.values

# Neural Net
mlp =  nn.MLPClassifier(hidden_layer_sizes=(8,)  \
                        , max_iter=1000 , alpha=1e-4  \
                        , solver='adam' , verbose=10  \
                        , tol=1e-19 , random_state=1  \
                        , learning_rate_init=.001)

nnModel = mlp.fit(trainData , trainLabel)

x = np.linspace(1, nnModel.n_iter_ , nnModel.n_iter_)

plt.plot(X2 , nnModel.loss_curve_, label = 'Convergence')
plt.title('Error Convergence ')
plt.ylabel('Cost function')
plt.xlabel('Iterations')
plt.legend()
plt.show()

print("Training set score for ADAM: %f" % mlp.score(trainData, trainLabel))
print("Test set score for ADAM: %f"     % mlp.score(testData , testLabel ))