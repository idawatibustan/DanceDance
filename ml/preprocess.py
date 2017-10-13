# plot timeseries data

import matplotlib as mpl
import numpy as np
import pandas as pd
from plot_helper import plot_frame, plot_gyro, plot_acc, plot_filter
from low_pass_filter import butter_lowpass_filter

# low_pass_filter params declaration
order = 1
fs = 25.0
cutoff = 3.667

def normalise_data(df_in):
    df_normalised = pd.DataFrame(preprocessing.normalize(df_in.values), columns=df_in.columns)
    return df_normalised

def low_pass_plotting(df_in): 
    t = df_in.index
    for col in df.columns.values:
        y = butter_lowpass_filter(df_in[col], cutoff, fs, order)
        plot_filter(t, df_in[col], y)

def low_pass(df_in):
    df_filtered = pd.DataFrame()
    t = df_in.index
    for col in df.columns.values:
        df_filtered[col] = butter_lowpass_filter(df_in[col], cutoff, fs, order)
    return df_filtered

# load data
dataset = pd.DataFrame()
csvfile = 'first_test.csv'
df = pd.read_csv(csvfile)

# split data

FREQ = 25
T_LEN = 2.4
L_FRAME = int( FREQ * T_LEN )
L_OVLAP = int( 0.5 * L_FRAME )
L_STEPS = L_FRAME - L_OVLAP

max_len = len(df.index)
for j in np.arange(0, max_len, L_STEPS):
    df_new = df[ j : j+L_FRAME ]
    df_filtered = low_pass(df_new)
    # plot_gyro(df_new)
    # plot_gyro(df_filtered)
    # plot_acc(df_new)
    # plot_acc(df_filtered)
    feats = ts.extract_feature( df_filtered )
    feats['label'] = "test"
    dataset = dataset.append( feats, ignore_index = True )

csvfile_new = csvfile.split(".")[0]+"_extracted.csv"
dataset.to_csv(csvfile_new, index_col=False)