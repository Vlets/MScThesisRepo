import pandas as pd
import RecommenderSystem.dataFiles.mockData as dataFiles
from RecommenderSystem.DataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
import time

dataFrameMock = pd.DataFrame(dataFiles.mockData)
dataFrameMock2 = pd.DataFrame(dataFiles.mockData2)
path = "/Users/george/PycharmProjects/scikitLiterallyLearn/RecommenderSystem/dataFiles/test2.json"

jsonTools = JsonProcessor()

# unsorted data
dataFrame = jsonTools.json_read(path)
dataFrame = jsonTools.filter_columns(dataFrame)

# normal data
sortedData = jsonTools.read_and_sort_data(path)

start = time.time()
mockResult = mfa.init_algorithm(sortedData)
end = time.time()
print(end - start, "- Sorted Data")


start = time.time()
mockResult2 = mfa.init_algorithm(dataFrame)
end = time.time()
print(end - start, "- Unsorted data")

