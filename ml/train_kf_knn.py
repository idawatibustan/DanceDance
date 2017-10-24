from os import makedirs
from os.path import exists
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from plot_helper import plot_confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle

if not exists('log'):
    makedirs('log')

def train_knn(train_set, test_set):
    trainData  = train_set.drop('label' , axis=1).values
    trainLabel = train_set.label.values
    
    testData  = test_set.drop('label' , axis=1).values
    testLabel = test_set.label.values
    
#     print("in : %s %s" % (len(train_set), len(test_set)))
#     print("unique train set", np.unique(train_set.label.values))
#     print("unique test set", np.unique(test_set.label.values))
#     print("type: %s %s" % (type(trainData), type(trainLabel)))
#     print("type: %s %s" % (type(testData), type(testLabel)))
    
    knnclf = knn(n_neighbors=10 , n_jobs=2 , weights='uniform')

    knnModel = knnclf.fit(trainData , trainLabel)

    train_conf = knnModel.score( trainData , trainLabel )
    test_conf = knnModel.score( testData  , testLabel )
#     print("Training set score for KNN: %f" % train_conf )
#     print("Testing  set score for KNN: %f" % test_conf )

    y_pred = knnModel.predict(testData)

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(testLabel, y_pred)
    
    log = activate_logger('train_knn', 'log/training_knn_info_complete.log')
    log.info("cnf_matrix\n %s" % cnf_matrix)

    return {'model': knnModel,
            'train_conf': train_conf,
            'test_conf': test_conf
           }

def activate_logger(name, filename):
    import logging
    logger = logging.getLogger(name)
    hdlr = logging.FileHandler(filename, 'w')
    formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s | %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == "__main__":
    # activate logger
    log = activate_logger('train_kf', 'log/training_knn_kf_info.log')
    
    # load processed data
    df = pd.read_csv('data_ext/full_checked_extracted.csv')

    # kf declare
    kf = KFold( n_splits=5, shuffle=True, random_state=None )
    count = 0
    mf = pd.DataFrame()
    
    for train_i, test_i in kf.split(df):
        # split dataset
        train = df.iloc[train_i]
        test = df.iloc[test_i]
        log.info("in : %s %s" % (len(train), len(test)))
        
        # ensure all unique label in training & testing
        train_l = np.unique(train.label.values)
        test_l = np.unique(test.label.values)
        if not(len(train_l)==11  and len(test_l)==11):
            log.warning("train/test: %d, %d" % ( len(train_l), len(test_l) ) )

        # get training model & conf
        res = train_knn(train, test)
        
        # add model & conf to table
        line = pd.DataFrame( data=res, index=[0] )
        line['round'] = count
        mf = mf.append( line, ignore_index = True )
        count += 1

    # sort_by max test_conf and train_conf
    mf = mf.sort_values(['train_conf', 'test_conf']).reset_index(drop=True)
    print mf
    log.info("model_table\n %s" % mf)
    
    # get model with max confidence, store
    top = mf.iloc[0]
    knnModel = top.model
    pickle.dump(knnModel, open('classifier/activities_kf.knn','wb'))
    log.info("Selected model %s with conf: %s, %s" % (top.round, top.train_conf, top.test_conf))