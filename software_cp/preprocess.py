#!/usr/bin/env python

import matplotlib as mpl
import numpy as np
import pandas as pd
import timeseries as ts

NUM_CSV = 15
L_FRAME = 128
L_OVLAP = 64
L_STEPS = L_FRAME - L_OVLAP

'''
plot 128 frame x y z data
with label of movement type
'''
def plot_frame(df):
    plt.figure(figsize=(4,3))
    plt.title(df.label.unique()[0])
    plt.plot(df['time'], df['x'])
    plt.plot(df['time'], df['y'])
    plt.plot(df['time'], df['z'])
    plt.show()

'''
ensure segmented frame is clean
if it has 128 data
from the same activity label
'''
def is_df_clean( df ):
    if len(df.index) < 128:
        return False
    labels = df.label.unique()
    if len(labels) > 1:
        return False
    return True

dataset = pd.DataFrame()

for i in range(1, NUM_CSV + 1):
    csvfile = 'dataset_1/' + str(i) + '.csv'
    print csvfile
    df = pd.read_csv(csvfile,names=['time','X','Y','Z','label'])
    max_len = len(df.index)
    for j in np.arange(0, max_len, L_STEPS):
        df_new = df[ j : j+L_FRAME ]
        if is_df_clean( df_new ):
            feats = ts.extract_feature( df_new )
            feats['part'] = i
            feats['label'] = df_new.label.unique()[0]
            dataset = dataset.append( feats, ignore_index = True )

dataset.to_csv('dataset.csv')