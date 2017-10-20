import pandas as pd
import numpy as np
from random import randint

# For testing only
sample_data = df = pd.DataFrame({'X': range(128), 'Y': [2*i for i in range(128)], 'Z': [5*i for i in range(128)]})
features = ["mean", "std", "max", "min", "median", "mad", "corr"]

def extract_feature(window):
    # Create empty dataframe
    df = pd.DataFrame()

    # window is a dataframe that contains 128 period of x y and z
    # if feature == "mean":
    df['meanX'] = [window.mean().X]
    df['meanY'] = [window.mean().Y]
    df['meanZ'] = [window.mean().Z]

# elif feature == "std":
    df['stdX'] = [window.std().X]
    df['stdY'] = [window.std().Y]
    df['stdZ'] = [window.std().Z]

# elif feature == "max":
    x = window['X'].max(axis=0)
    y = window['Y'].max(axis=0)
    z = window['Z'].max(axis=0)
    df['maxX'] = [x]
    df['maxY'] = [y]
    df['maxZ'] = [z]

# elif feature == "min":
    x = window['X'].min(axis=0)
    y = window['Y'].min(axis=0)
    z = window['Z'].min(axis=0)
    df['minX'] = [x]
    df['minY'] = [y]
    df['minZ'] = [z]


# elif feature == "median":
    df['medianX'] = [window.median().X]
    df['medianY'] = [window.median().Y]
    df['medianZ'] = [window.median().Z]

# elif feature == "mad":
    df['madX'] = [window.mad().X]
    df['madY'] = [window.mad().Y]
    df['madZ'] = [window.mad().Z]

# elif feature == "corr":
    corrXY = window['X'].corr(window['Y'])
    corrXZ = window['X'].corr(window['Z'])
    corrYZ = window['Y'].corr(window['Z'])
    df['corrX'] = [corrXY]
    df['corrY'] = [corrXZ]
    df['corrZ'] = [corrYZ]

    return df

def create_features_table():
    # features = ["meanX", "meanY", "meanZ", "stdX", "stdY", "stdZ", "maxX", "maxY", "maxZ", "minX", "minY", "minZ",]
    columns   = []
    for feature in features:
        if feature != "corr":
            columns.append(feature + "X")
            columns.append(feature + "Y")
            columns.append(feature + "Z")
        else:
            columns.append(feature + "XY")
            columns.append(feature + "XZ")
            columns.append(feature + "YZ")

    df = pd.DataFrame(columns = columns)
    return df


# def get_features(window):
#     features_table = create_features_table()
#     for feature in features:
#         feature_df = extract_feature(window, feature)
#         print feature_df
#         features_table.append(feature_df)
#     return features_table
