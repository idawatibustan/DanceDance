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

TRAINING_FILE="data_extracted_v3_1711131701"
TRAINING_FILEPATH='dataset/data_ext/'
TESTING_FILE="data_test_extracted_v3_1711110156"
TESTING_FILEPATH='dataset/data_ext_test/'
MODEL_FILE="dance_v3"
EXC_DANCER = 2

if not exists('log'):
    makedirs('log')
if isfile('log/'+MODEL_FILE+'.log'):
    remove('log/'+MODEL_FILE+'.log')

def train_knn(train_set, test_set, k):
    droplabels = ['label', 'dancer', 'collection']
    trainData  = train_set.drop(droplabels, axis=1).values
    trainLabel = train_set.label.values
    
    testData  = test_set.drop(droplabels, axis=1).values
    testLabel = test_set.label.values
    
    # knnclf = knn(n_neighbors=k)    
    knnclf = knn(n_neighbors=k , algorithm='ball_tree' , leaf_size=25 , n_jobs=2 , weights='distance')

    knnModel = knnclf.fit(trainData , trainLabel)

    train_conf = knnModel.score( trainData , trainLabel )
    test_conf = knnModel.score( testData  , testLabel )

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
    
    score = knn.score(testData , testLabel )
    print("Testing set score for KNN: %f" % score)
    y_pred = knn.predict(testData)
    cnf_matrix = confusion_matrix(testLabel, y_pred)
    return cnf_matrix, score

def plot_all_cnfmats(mats):
    classes = range(6)
    leng = len(mats)
    cols = 4
    rows = (leng-1)/cols + 1
    f, ax = plt.subplots( rows, cols, figsize=(12,8) )
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
        ax[col, row].set_ylabel('True label')
        ax[col, row].set_xlabel('Predicted label')
    f.tight_layout()
    # plt.show()

def plot_cnfmats(cm):
    classes = range(6)
    tick_marks = np.arange(len(classes))

    f, (ax1, ax2) = plt.subplots(1,2, figsize=(12,6))
    ax1.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax1.set_title("confusion_matrix")
    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax1.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    ax1.set_xticks(tick_marks, classes)
    ax1.set_yticks(tick_marks, classes)
    ax1.set_ylabel('True label')
    ax1.set_xlabel('Predicted label')

    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    ax2.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    ax2.set_title("normalized_confusion_matrix")
    fmt = '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        ax2.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    ax2.set_xticks(tick_marks, classes)
    ax2.set_yticks(tick_marks, classes)
    ax2.set_ylabel('True label')
    ax2.set_xlabel('Predicted label')

    f.tight_layout()
    # plt.show()

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

def kfoldcrossval(df, k):
    mf = pd.DataFrame()
    count = 0
    for i in range(3):
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
            res = train_knn(train, test, k)
            
            # add model & conf to table
            line = pd.DataFrame( data=res, index=[0] )
            line['round'] = count
            mf = mf.append( line, ignore_index = True )
            count += 1

    # sort_by max test_conf and train_conf
    mf = mf.sort_values('train_conf', ascending=False).reset_index(drop=True)
    mf = mf.sort_values('test_conf', ascending=False).reset_index(drop=True)
    print(mf)
    log.info("model_table\n %s" % mf)
    
    # get model with max confidence, store
    top = mf.iloc[0]
    knnModel = top.model
    pickle.dump(knnModel, open('classifier/'+MODEL_FILE+'.knn','wb'))
    log.info("Selected model %s with conf: %s, %s" % (top.round, top.train_conf, top.test_conf))

    print("*** Training Completed ***")
    return mf, knnModel

def test_model(knnModel):
    df = pd.read_csv(TRAINING_FILEPATH+TRAINING_FILE+'.csv')
    df = df[feature_list]
    """EXCLUDE DANCE MOVES"""
    # df = df.loc[df['label'] < 6]
    cnf_mats = []
    for i in range(1,9):
        print("Testing on excluded dancer:", i)
        df1 = df.loc[df['dancer'] == i]
        cm, score = test_classifier(knnModel, df1)
        cnf_mats.append(cm)
    plot_all_cnfmats(cnf_mats)

    df = pd.read_csv(TESTING_FILEPATH+TESTING_FILE+'.csv')
    df = df[feature_list]
    print("Testing on unseen dancer")
    cm, score = test_classifier(knnModel, df)
    plot_cnfmats(cm)
    return score

if __name__ == "__main__":
    # activate logger
    log = activate_logger('train_kf', 'log/'+MODEL_FILE+'.log', append=False)

    """ FEATURES FOR MOVES 1 - 5 """
    feature_list = [
    'mean_ax0', 'mean_az0', 'mean_ax1', 'mean_abs_ax0', 'mean_abs_az0',
    'mean_abs_az1', 'std_ax0', 'std_ay0', 'std_az0', 'std_ax1',
    'std_ay1', 'std_az1', 'std_gx0', 'std_gy0', 'std_gx1', 'std_gy1',
    'median_ax0', 'median_ay0', 'median_ax1', 'median_az1', 'mad_ax0',
    'mad_ay0', 'mad_az0', 'mad_ax1', 'mad_ay1', 'mad_az1', 'mad_gy0',
    'mad_gx1', 'mad_gy1', 'max_ax0', 'max_az0', 'max_ay1', 'max_az1',
    'max_gy0', 'max_gx1', 'min_ay0', 'min_ax1', 'min_az1', 'min_gy0',
    'min_gx1', 'range_az0', 'range_ax1', 'range_ay1', 'range_az1',
    'range_gy0', 'range_gx1', 'corr_ayz0', 'corr_axz1', 'corr_ayz1',
    'corr_gxy0', 'corr_ax1x0', 'corr_ax1y0', 'corr_ax1z0', 'corr_ay1x0',
    'corr_ay1y0', 'corr_ay1z0', 'corr_gy0y1',
    'label','dancer','collection']
    """ FEATURES 10 moves """
    feature_list = [
    'mean_ax0', 'mean_az0', 'mean_ax1', 'mean_az1', 'mean_gy1',
    'mean_abs_ax0', 'mean_abs_ay0', 'mean_abs_az0', 'mean_abs_ax1',
    'mean_abs_az1', 'mean_abs_gx1', 'mean_abs_gy1', 'std_ax0',
    'std_ay0', 'std_az0', 'std_ax1', 'std_ay1', 'std_az1', 'std_gx0',
    'std_gy0', 'std_gx1', 'std_gy1', 'median_ax0', 'median_az0',
    'median_ax1', 'median_az1', 'median_gy1', 'mad_ax0', 'mad_ay0',
    'mad_az0', 'mad_ax1', 'mad_ay1', 'mad_az1', 'mad_gx0', 'mad_gy0',
    'mad_gx1', 'mad_gy1', 'max_ax0', 'max_ay0', 'max_az0', 'max_ax1',
    'max_az1', 'max_gx0', 'max_gy0', 'max_gy1', 'min_ax0', 'min_ay0',
    'min_az0', 'min_ax1', 'min_az1', 'min_gx0', 'min_gy0', 'min_gx1',
    'min_gy1', 'range_ax0', 'range_ay0', 'range_az0', 'range_ax1',
    'range_ay1', 'range_az1', 'range_gx0', 'range_gy0', 'range_gx1',
    'range_gy1', 'corr_axz0', 'corr_ayz0', 'corr_axz1', 'corr_gxy0',
    'corr_ax1x0', 'corr_ay1x0', 'corr_ay1y0', 'corr_ay1z0', 'corr_az1x0',
    'label','dancer','collection']

    """ GET ALL COLUMNS """
    df2 = pd.read_csv(TRAINING_FILEPATH+TRAINING_FILE+'.csv')

    """ EXCLUDING SOME DANCERS """
    # df = df2.loc[df2['dancer'] != EXC_DANCER]

    """ EXCLUDING SOME LABELS """
    # df = df2.loc[df2['label'] < 6]
    df = df2

    """ REMOVE UNDESIRED COLUMNS """
    df = df[feature_list]
    print("Number of features", len(df.columns))

    neighbors = range(1,20)
    scores = []
    n_neigh = []
    for k in neighbors:
        mf, bestModel = kfoldcrossval(df, k)
        score = test_model(bestModel)
        scores.append(score)
        n_neigh.append(k)

    res['scores'] = time_ms
    res['n_neighbors'] = df.index
    f, ax = plt.subplots( 1 )
    sns.pointplot(
        x="n_neighbors",
        y="scores",
        data=res,
        ax=ax,
        color=sns.color_palette("Set2", 10)[3],
        scale=0.25, ci=.50
        )
    plt.show()