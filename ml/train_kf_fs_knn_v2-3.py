from os import makedirs, remove
from os.path import exists, isfile
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import KFold
from plot_helper import plot_confusion_matrix
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pickle
import itertools

TRAINING_V1_FILE="data_extracted_v1_1710291648"
TRAINING_FILE="data_extracted_v2_1710312018"
TRAINING_FILEPATH='dataset/data_ext/'
MODEL_FILE="dance_top5_v2-3"
EXC_DANCER = 2

if not exists('log'):
    makedirs('log')
if isfile('log/'+MODEL_FILE+'.log'):
    remove('log/'+MODEL_FILE+'.log')

def train_knn(train_set, test_set):
    droplabels = ['label', 'dancer', 'collection']
    trainData  = train_set.drop(droplabels, axis=1).values
    trainLabel = train_set.label.values
    
    testData  = test_set.drop(droplabels, axis=1).values
    testLabel = test_set.label.values
    
    # print("in : %s %s" % (len(train_set), len(test_set)))
    # print("unique train set", np.unique(train_set.label.values))
    # print("unique test set", np.unique(test_set.label.values))
    # print("type: %s %s" % (type(trainData), type(trainLabel)))
    # print("type: %s %s" % (type(testData), type(testLabel)))
    
    knnclf = knn(n_neighbors=10 , n_jobs=2 , weights='uniform')

    knnModel = knnclf.fit(trainData , trainLabel)

    train_conf = knnModel.score( trainData , trainLabel )
    test_conf = knnModel.score( testData  , testLabel )
    # print("Training set score for KNN: %f" % train_conf )
    # print("Testing  set score for KNN: %f" % test_conf )

    y_pred = knnModel.predict(testData)

    # Compute confusion matrix
    cnf_matrix = confusion_matrix(testLabel, y_pred)
    
    log = activate_logger('train_knn', 'log/'+MODEL_FILE+'_long.log')
    log.info("cnf_matrix\n %s" % cnf_matrix)

    return {'model': knnModel,
            'train_conf': train_conf,
            'test_conf': test_conf
           }

def test_classifier(knn, df):
    droplabels = ['label', 'dancer', 'collection']
    testData  = df.drop(droplabels , axis=1).values
    testLabel = df.label.values
    
    print("Testing set score for KNN: %f" % knn.score(testData , testLabel ))
    y_pred = knn.predict(testData)
    cnf_matrix = confusion_matrix(testLabel, y_pred)
    # np.set_printoptions(precision=2)
    return cnf_matrix

def plot_all_cnfmats(mats):
    leng = len(mats)
    cols = 3
    rows = (leng-1)/cols + 1
    f, ax = plt.subplots(rows, cols, figsize=(16,30))
    classes = range(0,11)
    tick_marks = np.arange(len(classes))
    for j in range(leng):
        cm = mats[j]
        row = j%cols
        col = j/cols
        ax[col, row].imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
        ax[col, row].set_title("Dancer " + str(j+1))
        fmt = 'd'
        thresh = cm.max() / 2.
        for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            ax[col, row].text(j, i, format(cm[i, j], fmt),
                     horizontalalignment="center",
                     color="white" if cm[i, j] > thresh else "black")
        ax[col, row].set_xticks(tick_marks, classes)
        ax[col, row].set_yticks(tick_marks, classes)
    # f.tight_layout()
    plt.show()

def activate_logger(name, filename, append=True):
    import logging
    logger = logging.getLogger(name)
    if append:
        hdlr = logging.FileHandler(filename)
    else:
        hdlr = logging.FileHandler(filename, 'w')
    formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s | %(message)s')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)
    return logger

if __name__ == "__main__":
    # activate logger
    log = activate_logger('train_kf', 'log/'+MODEL_FILE+'.log', append=False)
    feature_list = [
    'mean_ax0', 'mean_az0', 'mean_az1', 'mean_abs_ax0', 'mean_abs_gy1',
    'std_ay0', 'std_az0', 'std_ax1', 'std_ay1', 'std_az1', 'std_gx0',
    'std_gy0', 'std_gx1', 'std_gy1', 'median_ax0', 'mad_ay0', 'mad_az0',
    'mad_ay1', 'mad_az1', 'mad_gx0', 'mad_gy0', 'mad_gx1', 'mad_gy1',
    'max_az0', 'max_az1', 'max_gx0', 'max_gy0', 'max_gy1', 'min_ay0',
    'min_gx1', 'min_gy1', 'range_az0', 'range_ay1', 'range_az1',
    'range_gx0', 'range_gy0', 'range_gx1', 'range_gy1', 'corr_ayz0',
    'corr_ay1y0', 'corr_ay1z0',
    'label','dancer','collection']

    """GET COLUMNS from V2 exactly as in V1"""
    # df1_cols = pd.read_csv(TRAINING_FILEPATH+TRAINING_V1_FILE+'.csv', nrows=1).columns
    # load processed data
    # df2 = pd.read_csv(TRAINING_FILEPATH+TRAINING_FILE+'.csv', usecols=df1_cols)

    """ GET ALL COLUMNS """
    df2 = pd.read_csv(TRAINING_FILEPATH+TRAINING_FILE+'.csv')
    """ EXCLUDING SOME DANCERS """
    df = df2.loc[df2['dancer'] != EXC_DANCER]
    
    """ REMOVE UNDESIRED COLUMNS """
    # df = df.drop(droplist, axis=1)
    df = df[feature_list]
    print len(df.columns)

    mf = pd.DataFrame()
    count = 0
    for i in range(2):
        # kf declare
        kf = KFold( n_splits=5, shuffle=True, random_state=None )
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
    mf = mf.sort_values('train_conf', ascending=False).reset_index(drop=True)
    mf = mf.sort_values('test_conf', ascending=False).reset_index(drop=True)
    print mf
    log.info("model_table\n %s" % mf)
    
    # get model with max confidence, store
    top = mf.iloc[0]
    knnModel = top.model
    pickle.dump(knnModel, open('classifier/'+MODEL_FILE+'.knn','wb'))
    log.info("Selected model %s with conf: %s, %s" % (top.round, top.train_conf, top.test_conf))

    print "Training Completed"
    df = pd.read_csv(TRAINING_FILEPATH+TRAINING_FILE+'.csv')
    df = df[feature_list]
    cnf_mats = []
    for i in range(1,7):
        print "Testing on excluded dancer:", i
        df1 = df.loc[df['dancer'] == i]
        mats = test_classifier(knnModel, df1)
        cnf_mats.append(mats)
    plot_all_cnfmats(cnf_mats)