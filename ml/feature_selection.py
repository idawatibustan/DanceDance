from os.path import isfile, join
from sklearn.ensemble import ExtraTreesClassifier
import numpy as np
import pandas as pd

""" DECLARE SETTINGS AND PARAMS """
datapath = "dataset/data_ext"
filename = "data_extracted_v3_1711011902.csv"
cutoff_mode = 0		# 0 = cut n features | 1 = cut with threshold
N = 5
THRESH = 0.001


""" load dataset """
df = pd.read_csv(join(datapath, filename))
data = df.drop(['dancer','collection'], axis=1)

""" USE DATA WITH LABELS < 6 """
data = data.loc[data['label'] < 6]

# Feature Importance with Extra Trees Classifier
try:
	while True:
		""" load data and calculate feature importance """
		names = data.columns
		dataframe = data
		array = dataframe.values
		X = data.drop('label', axis=1)
		Y = data.label
		# feature extraction
		model = ExtraTreesClassifier()
		model.fit(X, Y)
		print(model.feature_importances_)
		x = model.feature_importances_

		cutoff = x.argsort()[:N]
		print N, "lowest importance =", x[cutoff[N-1]]
		if cutoff_mode == 0:
			""" cutoff n number of features """
			list_ = np.where(x > x[cutoff[N-1]], X.columns, 0)
		else:
			""" cutoff with threshold """
			list_ = np.where(x > THRESH, X.columns, 0)

		print "selected features"
		print list_
		print "initial len =", len(list_)

		""" generate new feature list"""
		index = np.argwhere(list_==0)
		list_f = np.delete(list_, index)
		print "updated len =", len(list_f)

		crop_data = raw_input("Crop data with shown list? [y/n]")
		""" crop data with new list_f """
		if crop_data.lower() == 'y':
			list_f = np.append(list_f, 'label')
			data = data[list_f]

except KeyboardInterrupt:
	print "\nfinal selected features"
	print list_f
	exit()
