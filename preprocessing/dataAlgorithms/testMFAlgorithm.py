import pandas as pd
import preprocessing.dataFiles.mockData as dataFiles
from preprocessing.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.helpers.JsonProcessor import JsonProcessor
import time

dataFrameMock = pd.DataFrame(dataFiles.mockData)
dataFrameMock2 = pd.DataFrame(dataFiles.mockData2)

jsonTools = JsonProcessor()
dataFrame = jsonTools.json_read("/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json")

sortBy = ["visitorId", "timestamp"]
sortedData = jsonTools.json_sort(dataFrame, sortBy)

start = time.time()
mockResult = mfa.init_algorithm(sortedData)
end = time.time()
print(end - start)


start = time.time()
mockResult2 = mfa.init_algorithm(dataFrame)
end = time.time()
print(end - start)

