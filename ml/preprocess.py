# plot timeseries data

from os import listdir
from os.path import isfile, join
# import matplotlib as mpl
import numpy as np
import pandas as pd
import timeseries as ts
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

# segment param
FREQ = 60
T_LEN = 2.4
L_FRAME = int( FREQ * T_LEN )
L_OVLAP = int( 0.5 * L_FRAME )
L_STEPS = L_FRAME - L_OVLAP

# data paths
datapath = 'data_rec'
data_ex = 'data_ext'
if not os.path.exists(data_ex):
    os.makedirs(data_ex)

if __name__ = "__main__":

    # load data
    csvfiles = [ f for f in listdir(datapath) if isfile(join(datapath, f)) and '.csv' in f ]
    df_ext_all = pd.DataFrame()
    
    # iterate through all files
    # load it to df
    for f in csvfiles:
        dataset = pd.DataFrame()

        # load file
        csvfile = join(datapath,f)
        df = pd.read_csv(csvfile)

        # do something to df
        label = f.split("_")[0] 
        print label

        # splitting up lines & perform extraction
        max_len = len(df.index)
        for j in np.arange(0, max_len, L_STEPS):
            # get & plot segment
            df_new = df[ j : j+L_FRAME ]
            plot_gyro(df_new)
            plot_acc(df_new)
#            df_filtered = low_pass(df_new)
#            plot_gyro(df_filtered)
#            plot_acc(df_filtered)

            # extract feature
            feats = ts.extract_feature( df_new )
            # add label column
            feats['label'] = label
            dataset = dataset.append( feats, ignore_index = True )

        # saving dataset to file_extracted.csv
        csvfile_new = join( data_ex, csvfile.split(".")[0]+"_extracted.csv" )
        dataset.to_csv( csvfile_new, index_col=False )

        # append to cobined dataframe
        df_ext_all = pd.concat([df_ext_all, dataset])

    # save combined dataframe -> df_ext_all
    csv_all = join( data_ex, "full_dataset_extracted.csv" )
    df_ext_all.to_csv( csv_all, index_col=False )