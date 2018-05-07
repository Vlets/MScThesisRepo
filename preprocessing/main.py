from preprocessing.JsonProcessor import JsonProcessor
import pandas as pd
import numpy as np
from kmodes.kprototypes import KPrototypes
from pandas.io.json import json_normalize

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/testProduced.json"

sortBy = ["visitorId", "timestamp"]
categoricalData = ["audience", "visitorId", "channel", "url", "geo", "newVisit"]

data = jsonTools.json_read(filePath)
sortedData = jsonTools.json_sort(data, sortBy)

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
jsonTools.json_save(sortedData, "./testProduced", False)

#km = KPrototypes(n_clusters=4, init='Cao', verbose=16)

#clusters = km.fit_predict(sortedData, categorical=categoricalData)

#print(km.cluster_centroids_)