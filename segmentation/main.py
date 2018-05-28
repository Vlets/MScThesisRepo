from segmentation.helpers.JsonProcessor import JsonProcessor
import segmentation.dataFiles.mockData as dataFiles
import pandas as pd
import time
from kmodes.kmodes import KModes

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/largeFileAfterPP.json'

# THE ONE FUNCTION TO RULE THEM ALL IS do_it_all(filePath)

start = time.time()
data_frame = jsonTools.pre_process(bigData)
end = time.time()
data_frame = jsonTools.remove_homepage_and_stringify(data_frame)
data_frame = data_frame.drop('visitorId', axis=1)
print("Elapsed time:", (end - start) / 60, "Minutes (", (end - start), "Seconds )")

kmodes_cao = KModes(n_clusters=5, init='Cao', verbose=1)
kmodes_cao.fit(data_frame)

column_names = list(data_frame.columns.values)
clusters = pd.DataFrame(kmodes_cao.cluster_centroids_, columns=column_names)

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)

