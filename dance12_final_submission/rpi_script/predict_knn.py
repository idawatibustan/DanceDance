import preprocess
# import first_activities
import timeseries as ts
import pickle
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix
# from plot_helper import plot_confusion_matrix

# csvfile = 'test.csv'
# df = pd.read_csv(csvfile)

MILESTONE = 2
# indicate milestone to decide on number of dance to be classified
# milestone 1 = 5 moves
# milestone 2 = 10 moves

if MILESTONE == 1:
    loaded_knn = pickle.load(open('classifier/dance_top5_v3.knn','rb'))
elif MILESTONE == 2:
    loaded_knn = pickle.load(open('classifier/dance_v3.knn','rb'))

def is_clean(df_):
    if np.any(pd.isnull(df_)):
        return False
    return True

def process_data(window):
    # Do low pass filter here
    # feats = ts.extract_feature( window )
    # feats = ts.extract_feature_upgrade( window )
    if MILESTONE == 1:
        feats = ts.extract_feature_v3( window )
    elif MILESTONE == 2:
        feats = ts.extract_feature_v4( window )
    if not is_clean(feats):
        raise ValueError("NaN data found, window can't be processed")
    return feats

def predict(df):
    try:
        f = process_data(df)
    except ValueError as e:
        print "ValueError:", e
        return 12
    except AttributeError as e:
        print "AttributeError:", e
        return 12
    except Exception as e:
        print "Exception:", e
        return 12
    result = loaded_knn.predict(f)
    return result[0]

def predict_prob(df):
    try:
        f = process_data(df)
    except ValueError as e:
        print "ValueError:", e
        return 12
    except AttributeError as e:
        print "AttributeError:", e
        return 12
    except Exception as e:
        print "Exception:", e
        return 12
    result = loaded_knn.predict_proba(f)
    i = np.argmax(result)
    c = result[0][i]
    return i, c

# if __name__ == "__main__":
#     r = predict(df)
#     print type(r)
#     print r[0]
#     print type(r[0])
