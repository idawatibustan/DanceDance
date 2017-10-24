import preprocess
# import first_activities
import timeseries as ts
import pickle
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier as knn
from sklearn.metrics import confusion_matrix
from plot_helper import plot_confusion_matrix

csvfile = 'test.csv'
df = pd.read_csv(csvfile)

def process_data(window):
    # Do low pass filter here
    feats = ts.extract_feature( window )
    # feats['label'] = label
    return feats



def main():
    # f = pd.DataFrame()
    f = process_data(df)
    loaded_knn = pickle.load(open('first_activities.knn','rb'))
    result = loaded_knn.predict(f)
    print result
    # ext_data = process_data(window)
    # y_pred = first_activities.predict(testData)


if __name__ == '__main__':
    main()
