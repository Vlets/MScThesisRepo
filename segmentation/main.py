import time
import pandas as pd
from kmodes.kmodes import KModes
from sklearn.metrics import silhouette_score
from segmentation.helpers.JsonProcessor import JsonProcessor
from segmentation.helpers import urlKeywordExtractor as urlExtract

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/largeFileAfterPP.json'

# THE ONE FUNCTION TO RULE THEM ALL IS pipeline(filePath)

data_frame = jsonTools.pre_process(filePath)

data_frame = data_frame.drop(['geo.country', 'transactionPath'], axis=1)
data_frame = data_frame.astype(str)

kmodes_cao = KModes(n_clusters=10, init='Cao', verbose=1)
kmodes_cao.fit_predict(data_frame)

column_names = list(data_frame.columns.values)
clusters = pd.DataFrame(kmodes_cao.cluster_centroids_, columns=column_names)

a = pd.read_csv(
    "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/8juneSmallPCM.csv")
b = kmodes_cao.labels_
print("Silhouette score:", silhouette_score(a, b, metric='precomputed'))

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", to_json=False)
