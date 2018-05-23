from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles
import pandas as pd
import time
from kmodes.kmodes import KModes

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/finalDataDropped.json'

# THE ONE FUNCTION TO RULE THEM ALL IS do_it_all(filePath)

start = time.time()
clusters = jsonTools.pipeline(bigData)
end = time.time()
print("Elapsed time:", (end - start) / 60, "Minutes (", (end - start), "Seconds )")

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)

