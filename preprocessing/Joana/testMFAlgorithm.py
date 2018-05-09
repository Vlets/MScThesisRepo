import pandas as pd
import preprocessing.dataFiles.mockData as dataFiles
from preprocessing.Joana.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.helpers.JsonProcessor import JsonProcessor


dataFrameMock = pd.DataFrame(dataFiles.mockData)
dataFrameMock2 = pd.DataFrame(dataFiles.mockDataReordered)

jsonTools = JsonProcessor()
#dataFrame = jsonTools.json_read("/Users/Joana/Documents/GitHub/scikitLiterallyLearn/preprocessing/Joana/test2.json")

sortBy = ["visitorId", "timestamp"]
sortedData = jsonTools.json_sort(dataFrameMock, sortBy)
sortedData2 = jsonTools.json_sort(dataFrameMock2, sortBy)

mockResult = mfa.init_algorithm(sortedData)


