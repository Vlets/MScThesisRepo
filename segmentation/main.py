import time
import pandas as pd
from segmentation.helpers.JsonProcessor import JsonProcessor
from segmentation.helpers import urlKeywordExtractor as urlExtract


jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/largeFileAfterPP.json'

# THE ONE FUNCTION TO RULE THEM ALL IS pipeline(filePath)

start = time.time()
data_frame = jsonTools.pre_process(bigData)

data_frame = jsonTools.remove_homepage_and_stringify(data_frame)
data_frame['keys'] = data_frame.transactionPath.apply(urlExtract.get_keywords)

data_frame = data_frame.drop(['visitorId', 'geo.country', 'userAgent'], axis=1)
data_frame = data_frame.astype(str)

end = time.time()
print("Elapsed time:", (end - start) / 60, "Minutes (", (end - start), "Seconds )")


clusters = jsonTools.cluster_data(data_frame, 8)
end = time.time()
print("Total Elapsed time:", (end - start) / 60, "Minutes (", (end - start), "Seconds )")
# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)

