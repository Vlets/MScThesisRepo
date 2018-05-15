import pandas as pd
import preprocessing.dataFiles.mockData as dataFiles
from preprocessing.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.helpers.JsonProcessor import JsonProcessor
import time

dataFrameMock = pd.DataFrame(dataFiles.mockData)
dataFrameMock2 = pd.DataFrame(dataFiles.mockData2)
path = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"

jsonTools = JsonProcessor()

# unsorted data
dataFrame = jsonTools.json_read(path)
dataFrame = jsonTools.normalize_collectors(dataFrame)

# normal data
sortedData = jsonTools.do_it_all(path)

start = time.time()
mockResult = mfa.init_algorithm(sortedData)
end = time.time()
print(end - start, "- Sorted Data")


start = time.time()
mockResult2 = mfa.init_algorithm(dataFrame)
end = time.time()
print(end - start, "- Unsorted data")

