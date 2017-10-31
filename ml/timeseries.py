import pandas as pd
import numpy as np
from random import randint

# For testing only
# sample_data = df = pd.DataFrame({'X': range(128), 'Y': [2*i for i in range(128)], 'Z': [5*i for i in range(128)]})
# features = ["mean", "std", "max", "min", "median", "mad", "corr"]

def extract_feature(window):
    # ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1

    # Store extracted data into df
    df = pd.DataFrame()

    # window is a dataframe that contains 128 period of x y and z

    # Mean data
    df['mean_ax0'] = [window.mean().ax0]
    df['mean_ay0'] = [window.mean().ay0]
    df['mean_az0'] = [window.mean().az0]
    df['mean_ax1'] = [window.mean().ax1]
    df['mean_ay1'] = [window.mean().ay1]
    df['mean_az1'] = [window.mean().az1]

    df['mean_gx0'] = [window.mean().gx0]
    df['mean_gy0'] = [window.mean().gy0]
    # df['mean_gz0'] = [window.mean().gz0]
    df['mean_gx1'] = [window.mean().gx1]
    df['mean_gy1'] = [window.mean().gy1]
    # df['mean_gz1'] = [window.mean().gz1]

    # STD data
    df['std_ax0'] = [window.std().ax0]
    df['std_ay0'] = [window.std().ay0]
    df['std_az0'] = [window.std().az0]
    df['std_ax1'] = [window.std().ax1]
    df['std_ay1'] = [window.std().ay1]
    df['std_az1'] = [window.std().az1]

    df['std_gx0'] = [window.std().gx0]
    df['std_gy0'] = [window.std().gy0]
    # df['std_gz0'] = [window.std().gz0]
    df['std_gx1'] = [window.std().gx1]
    df['std_gy1'] = [window.std().gy1]
    # df['std_gz1'] = [window.std().gz1]

    # Median data
    df['median_ax0'] = [window.median().ax0]
    df['median_ay0'] = [window.median().ay0]
    df['median_az0'] = [window.median().az0]
    df['median_ax1'] = [window.median().ax1]
    df['median_ay1'] = [window.median().ay1]
    df['median_az1'] = [window.median().az1]

    df['median_gx0'] = [window.median().gx0]
    df['median_gy0'] = [window.median().gy0]
    # df['median_gz0'] = [window.median().gz0]
    df['median_gx1'] = [window.median().gx1]
    df['median_gy1'] = [window.median().gy1]
    # df['median_gz1'] = [window.median().gz1]

    # Mad data
    df['mad_ax0'] = [window.mad().ax0]
    df['mad_ay0'] = [window.mad().ay0]
    df['mad_az0'] = [window.mad().az0]
    df['mad_ax1'] = [window.mad().ax1]
    df['mad_ay1'] = [window.mad().ay1]
    df['mad_az1'] = [window.mad().az1]

    df['mad_gx0'] = [window.mad().gx0]
    df['mad_gy0'] = [window.mad().gy0]
    # df['mad_gz0'] = [window.mad().gz0]
    df['mad_gx1'] = [window.mad().gx1]
    df['mad_gy1'] = [window.mad().gy1]
    # df['mad_gz1'] = [window.mad().gz1]

    # Max
    df['max_ax0'] = [window['ax0'].max(axis=0)]
    df['max_ay0'] = [window['ay0'].max(axis=0)]
    df['max_az0'] = [window['az0'].max(axis=0)]
    df['max_ax1'] = [window['ax1'].max(axis=0)]
    df['max_ay1'] = [window['ay1'].max(axis=0)]
    df['max_az1'] = [window['az1'].max(axis=0)]

    df['max_gx0'] = [window['gx0'].max(axis=0)]
    df['max_gy0'] = [window['gy0'].max(axis=0)]
    # df['max_gz0'] = [window['gz0'].max(axis=0)]
    df['max_gx1'] = [window['gx1'].max(axis=0)]
    df['max_gy1'] = [window['gy1'].max(axis=0)]
    # df['max_gz1'] = [window['gz1'].max(axis=0)]

    # Min
    df['min_ax0'] = [window['ax0'].min(axis=0)]
    df['min_ay0'] = [window['ay0'].min(axis=0)]
    df['min_az0'] = [window['az0'].min(axis=0)]
    df['min_ax1'] = [window['ax1'].min(axis=0)]
    df['min_ay1'] = [window['ay1'].min(axis=0)]
    df['min_az1'] = [window['az1'].min(axis=0)]

    df['min_gx0'] = [window['gx0'].min(axis=0)]
    df['min_gy0'] = [window['gy0'].min(axis=0)]
    # df['min_gz0'] = [window['gz0'].min(axis=0)]
    df['min_gx1'] = [window['gx1'].min(axis=0)]
    df['min_gy1'] = [window['gy1'].min(axis=0)]
    # df['min_gz1'] = [window['gz1'].min(axis=0)]


    # Corr
    df['corr_axy0'] = [window['ax0'].corr(window['ay0'])]
    df['corr_axz0'] = [window['ax0'].corr(window['az0'])]
    df['corr_ayz0'] = [window['ay0'].corr(window['az0'])]
    df['corr_axy1'] = [window['ax1'].corr(window['ay1'])]
    df['corr_axz1'] = [window['ax1'].corr(window['az1'])]
    df['corr_ayz1'] = [window['ay1'].corr(window['az1'])]

    df['corr_gxy0'] = [window['gx0'].corr(window['gy0'])]
    # df['corr_gxz0'] = [window['gx0'].corr(window['gz0'])]
    # df['corr_gyz0'] = [window['gy0'].corr(window['gz0'])]
    df['corr_gxy1'] = [window['gx1'].corr(window['gy1'])]
    # df['corr_gxz1'] = [window['gx1'].corr(window['gz1'])]
    # df['corr_gyz1'] = [window['gy1'].corr(window['gz1'])]

    return df

def extract_feature_upgrade(window):
    # ax0,ay0,az0,gx0,gy0,gz0,ax1,ay1,az1,gx1,gy1,gz1

    # Store extracted data into df
    df = pd.DataFrame()

    # window is a dataframe that contains 128 period of x y and z

    # Mean data
    df['mean_ax0'] = [window.ax0.values.mean()]
    df['mean_ay0'] = [window.ay0.values.mean()]
    df['mean_az0'] = [window.az0.values.mean()]
    df['mean_ax1'] = [window.ax1.values.mean()]
    df['mean_ay1'] = [window.ay1.values.mean()]
    df['mean_az1'] = [window.az1.values.mean()]

    df['mean_gx0'] = [window.gx0.values.mean()]
    df['mean_gy0'] = [window.gy0.values.mean()]
    # df['mean_gz0'] = [window.gz0.values.mean()]
    df['mean_gx1'] = [window.gx1.values.mean()]
    df['mean_gy1'] = [window.gy1.values.mean()]
    # df['mean_gz1'] = [window.gz1.values.mean()]

    # Mean data
    df['mean_abs_ax0'] = df['mean_ax0'].abs().values
    df['mean_abs_ay0'] = df['mean_ay0'].abs().values
    df['mean_abs_az0'] = df['mean_az0'].abs().values
    df['mean_abs_ax1'] = df['mean_ax1'].abs().values
    df['mean_abs_ay1'] = df['mean_ay1'].abs().values
    df['mean_abs_az1'] = df['mean_az1'].abs().values

    df['mean_abs_gx0'] = df['mean_gx0'].abs().values
    df['mean_abs_gy0'] = df['mean_gy0'].abs().values
    # df['mean_abs_gz0'] = df['mean_gz0'].abs().values
    df['mean_abs_gx1'] = df['mean_gx1'].abs().values
    df['mean_abs_gy1'] = df['mean_gy1'].abs().values
    # df['mean_abs_gz1'] = df['mean_gz1'].abs().values

    # STD data
    df['std_ax0'] = [window.ax0.values.std()]
    df['std_ay0'] = [window.ay0.values.std()]
    df['std_az0'] = [window.az0.values.std()]
    df['std_ax1'] = [window.ax1.values.std()]
    df['std_ay1'] = [window.ay1.values.std()]
    df['std_az1'] = [window.az1.values.std()]

    df['std_gx0'] = [window.gx0.values.std()]
    df['std_gy0'] = [window.gy0.values.std()]
    # df['std_gz0'] = [window.gz0.values.std()]
    df['std_gx1'] = [window.gx1.values.std()]
    df['std_gy1'] = [window.gy1.values.std()]
    # df['std_gz1'] = [window.gz1.values.std()]

    # Median data
    df['median_ax0'] = [np.median(window.ax0.values)]
    df['median_ay0'] = [np.median(window.ay0.values)]
    df['median_az0'] = [np.median(window.az0.values)]
    df['median_ax1'] = [np.median(window.ax1.values)]
    df['median_ay1'] = [np.median(window.ay1.values)]
    df['median_az1'] = [np.median(window.az1.values)]

    df['median_gx0'] = [np.median(window.gx0.values)]
    df['median_gy0'] = [np.median(window.gy0.values)]
    # df['median_gz0'] = [np.median(window.gz0.values)]
    df['median_gx1'] = [np.median(window.gx1.values)]
    df['median_gy1'] = [np.median(window.gy1.values)]
    # df['median_gz1'] = [np.median(window.gz1.values)]

    # Mad data
    mads = window.mad()
    df['mad_ax0'] = [mads.ax0]
    df['mad_ay0'] = [mads.ay0]
    df['mad_az0'] = [mads.az0]
    df['mad_ax1'] = [mads.ax1]
    df['mad_ay1'] = [mads.ay1]
    df['mad_az1'] = [mads.az1]

    df['mad_gx0'] = [mads.gx0]
    df['mad_gy0'] = [mads.gy0]
    # df['mad_gz0'] = [mads.gz0]
    df['mad_gx1'] = [mads.gx1]
    df['mad_gy1'] = [mads.gy1]
    # df['mad_gz1'] = [mads.gz1]

    # Max
    df['max_ax0'] = [window.ax0.values.max()]
    df['max_ay0'] = [window.ay0.values.max()]
    df['max_az0'] = [window.az0.values.max()]
    df['max_ax1'] = [window.ax1.values.max()]
    df['max_ay1'] = [window.ay1.values.max()]
    df['max_az1'] = [window.az1.values.max()]

    df['max_gx0'] = [window.gx0.values.max()]
    df['max_gy0'] = [window.gy0.values.max()]
    # df['max_gz0'] = [window.gz0.values.max()]
    df['max_gx1'] = [window.gx1.values.max()]
    df['max_gy1'] = [window.gy1.values.max()]
    # df['max_gz1'] = [window.gz1.values.max()]

    # Min
    df['min_ax0'] = [window.ax0.values.min()]
    df['min_ay0'] = [window.ay0.values.min()]
    df['min_az0'] = [window.az0.values.min()]
    df['min_ax1'] = [window.ax1.values.min()]
    df['min_ay1'] = [window.ay1.values.min()]
    df['min_az1'] = [window.az1.values.min()]

    df['min_gx0'] = [window.gx0.values.min()]
    df['min_gy0'] = [window.gy0.values.min()]
    # df['min_gz0'] = [window.gz0.values.min()]
    df['min_gx1'] = [window.gx1.values.min()]
    df['min_gy1'] = [window.gy1.values.min()]
    # df['min_gz1'] = [window.gz1.values.min()]

    # Range
    df['range_ax0'] = df['max_ax0'].values - df['min_ax0'].values
    df['range_ay0'] = df['max_ay0'].values - df['min_ay0'].values
    df['range_az0'] = df['max_az0'].values - df['min_az0'].values
    df['range_ax1'] = df['max_ax1'].values - df['min_ax1'].values
    df['range_ay1'] = df['max_ay1'].values - df['min_ay1'].values
    df['range_az1'] = df['max_az1'].values - df['min_az1'].values

    df['range_gx0'] = df['max_gx0'].values - df['min_gx0'].values
    df['range_gy0'] = df['max_gy0'].values - df['min_gy0'].values
    # df['range_gz0'] = df['max_gz0'].values - df['min_gz0'].values
    df['range_gx1'] = df['max_gx1'].values - df['min_gx1'].values
    df['range_gy1'] = df['max_gy1'].values - df['min_gy1'].values
    # df['range_gz1'] = df['max_gz1'].values - df['min_gz1'].values

    # Corr
    df['corr_axy0'] = np.correlate(window.ax0.values, window.ay0.values)[0]
    df['corr_axz0'] = np.correlate(window.ax0.values, window.az0.values)[0]
    df['corr_ayz0'] = np.correlate(window.ay0.values, window.az0.values)[0]
    df['corr_axy1'] = np.correlate(window.ax1.values, window.ay1.values)[0]
    df['corr_axz1'] = np.correlate(window.ax1.values, window.az1.values)[0]
    df['corr_ayz1'] = np.correlate(window.ay1.values, window.az1.values)[0]

    df['corr_gxy0'] = np.correlate(window.gx0.values, window.gy0.values)[0]
    # df['corr_gxz0'] = np.correlate(window.gx0.values, window.gz0.values)[0]
    # df['corr_gyz0'] = np.correlate(window.gy0.values, window.gz0.values)[0]
    df['corr_gxy1'] = np.correlate(window.gx1.values, window.gy1.values)[0]
    # df['corr_gxz1'] = np.correlate(window.gx1.values, window.gz1.values)[0]
    # df['corr_gyz1'] = np.correlate(window.gy1.values, window.gz1.values)[0]

    return df
