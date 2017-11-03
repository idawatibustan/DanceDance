# plot timeseries data
import os
from os import listdir, makedirs
from os.path import isfile, join, basename,exists
# import matplotlib as mpl
import numpy as np
import pandas as pd
import timeseries as ts
import time
from low_pass_filter import butter_lowpass_filter
from plot_helper import plot_frame, plot_gyro, plot_acc, plot_filter

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

def is_clean(df):
    if np.any(pd.isnull(df)):
        return False
    return True

# segment param
FREQ = 60                       # Hz
T_LEN = 2.4                     # seconds
L_FRAME = int( FREQ * T_LEN )   # window size
L_OVLAP = int( 0.5 * L_FRAME )  # overlap size
L_STEPS = L_FRAME - L_OVLAP

# data paths
datapath = 'dataset/data_rec'
data_ex = 'dataset/data_ext'
if not exists(data_ex):
    makedirs(data_ex)

def segment_extract(df):
    # splitting up lines & perform extraction
    max_len = len(df.index)
    dataset = pd.DataFrame()
    for j in np.arange(0, max_len, L_STEPS):
        # get segment
        df_new = df[ j : j+L_FRAME ]

        # extract feature
        feats = ts.extract_feature_upgrade( df_new )

        if is_clean(feats):
            dataset = dataset.append( feats, ignore_index = True )

    return dataset

if __name__ == "__main__":
    filtering_on = False        # set before running

    # load data
    csvfiles = [ f for f in listdir(datapath) if isfile(join(datapath, f)) and '.csv' in f ]
    df_ext_all = pd.DataFrame()

    # iterate through all files
    # load it to df
    for f in csvfiles:

        # load file
        csvfile = join(datapath,f)
        df = pd.read_csv(csvfile)

        fnames = f.split(".")[0].split("_")
        # do something to df
        label = fnames[0]
        collection = fnames[2]
        dancer = fnames[4]
        print "Working on movement: %s by dancer: %s on %s" % (label, dancer, collection)

        if filtering_on:
            df_filtered1 = low_pass(df)
            df_filtered = df_filtered1.iloc[10:]
            extracted = segment_extract(df_filtered)
        else:
            extracted = segment_extract(df)

        # add information columns
        extracted['label'] = label
        extracted['dancer'] = dancer
        extracted['collection'] = collection
        # append to cobined dataframe
        df_ext_all = pd.concat([df_ext_all, extracted])

    # save combined dataframe -> df_ext_all
    timestr = time.strftime("%y%m%d%H%M")
    if filtering_on:
        csvname = "data_filtered_extracted_v2_" + timestr + ".csv"
    else:
        csvname = "data_extracted_v2_" + timestr + ".csv"
    csv_all = join( data_ex, csvname)
    df_ext_all.to_csv( csv_all, index=False )