from segmentation.helpers.JsonProcessor import JsonProcessor
import segmentation.dataFiles.mockData as dataFiles
import pandas as pd
import time
from kmodes.kmodes import KModes

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/finalDataDropped.json'

# THE ONE FUNCTION TO RULE THEM ALL IS do_it_all(filePath)

start = time.time()
clusters = jsonTools.pipeline(filePath)
end = time.time()
print("Elapsed time:", (end - start) / 60, "Minutes (", (end - start), "Seconds )")

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)

