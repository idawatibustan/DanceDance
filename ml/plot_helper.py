import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def plot_frame(df):
    for col in df.columns.values:
        plt.figure(figsize=(16,3))
        plt.title(col)
        plt.plot(df.index, df[col])
        plt.show()

def plot_gyro(df, label=None):
    gyros = [['gx0','gy0','gz0'],['gx1','gy1','gz1']]
    for num in gyros:
        plt.figure(figsize=(16,3))
        if label:
            plt.title("%s - gyro %s" % (label, num))
            plt.legend()
        else:
            plt.title("gyro %s" % num)
            plt.legend()
        for col in num:
            plt.plot(df.index, df[col])
        plt.show()
        
def plot_acc(df, label=None):
    accs = [['ax0','ay0','az0'],['ax1','ay1','az1']]
    for num in accs:
        plt.figure(figsize=(16,3))
        if label:
            plt.title("%s - acc %s" % (label, num))
        else:
            plt.title("acc %s" % num)
        for col in num:
            plt.plot(df.index, df[col])
        plt.show()
        
def plot_sensor(df, label=None):
    sensors = [['gx0','gy0','gz0'],['gx1','gy1','gz1'],['ax0','ay0','az0'],['ax1','ay1','az1']]
    f, ax = plt.subplots( 2, 2, figsize=(20,10), sharey=True, sharex=True)
    for i in range(4):
        if label:
            plt.title("%s - acc %s" % (label, sensors[i]))
        else:
            plt.title("acc %s" % sensors[i])
        for col in sensors[i]:
            ax[i/2, i%2].plot(df.index, df[col])
            ax[i/2, i%2].set_title( str(sensors[i]) )
    plt.show()

def plot_filter(t, old, new):
    plt.figure(figsize=(16,3))
    plt.plot(t, old, 'b-', label='data')
    plt.plot(t, new, 'g-', linewidth=2, label='filtered data')
    plt.legend()
    plt.show()

def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')