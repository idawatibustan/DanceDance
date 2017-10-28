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
loaded_knn = pickle.load(open('classifier/activities_kf.knn','rb'))

def is_clean(df_):
    if np.any(pd.isnull(df_)):
        return False
    return True

def process_data(window):
    # Do low pass filter here
    feats = ts.extract_feature( window )
    if not is_clean(feats):
        raise ValueError("NaN data found, window can't be processed")
    return feats

def predict(df):
    try:
        f = process_data(df)
    except ValueError as e:
        print "ValueError:", e
        return 11
    except AttributeError as e:
        print "AttributeError:", e
        return 11
    except Exception as e:
        print "Exception:", e
        return 11
    result = loaded_knn.predict(f)
    return result[0]

# if __name__ == "__main__":
#     r = predict(df)
#     print type(r)
#     print r[0]
#     print type(r[0])
