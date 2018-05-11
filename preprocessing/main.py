from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles
import pandas as pd
import json
from pandas.io.json import json_normalize
import time

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"
sortBy = ["visitorId", "timestamp"]

data = jsonTools.json_read(filePath)
# TODO: normalise other columns too
collectorData = json_normalize(data['collectorData'])
fusedData = pd.concat([collectorData, data], axis=1)
allData = fusedData.drop(['collectorData'], axis=1)
sortedData = jsonTools.json_sort(allData, sortBy)


# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)
