from preprocessing.JsonProcessor import JsonProcessor
import numpy as np
from kmodes.kprototypes import KPrototypes

jsonTools = JsonProcessor()

filePath = "/Users/george/Expendable/sample.json"

sortBy = ["visitorId", "timestamp"]
categoricalData = ["audience", "visitorId", "channel", "url", "geo", "newVisit"]

data = jsonTools.json_read(filePath)
sortedData = jsonTools.json_sort(data, sortBy)

# Save to Json
# jsonTools.json_save(sortedData, "./testProduced.json")

#km = KPrototypes(n_clusters=4, init='Cao', verbose=16)

#clusters = km.fit_predict(sortedData, categorical=categoricalData)

#print(km.cluster_centroids_)