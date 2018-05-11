from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles
import pandas as pd
import json
from pandas.io.json import json_normalize
import time

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"
sortBy = ["visitorId", "timestamp"]

###### Start timing method 1
start = time.time()

with open(filePath) as f:
    file = json.load(f)
    normalisedFile = json_normalize(file)

sortedData1 = jsonTools.json_sort(normalisedFile, sortBy)
end = time.time()
print(end - start, "Seconds")
###### Stop timing method 1

###### Start timing method 2
start = time.time()

data = jsonTools.json_read(filePath)
# TODO: normalise other columns too
collectorData = json_normalize(data['collectorData'])
allData = pd.concat([collectorData, data])
sortedData = jsonTools.json_sort(allData, sortBy)

end = time.time()
print(end - start, "Seconds")


# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)
