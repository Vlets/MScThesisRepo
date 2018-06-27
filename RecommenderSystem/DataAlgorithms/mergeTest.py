import pandas as pd
import RecommenderSystem.dataFiles.mockData as dataFiles
from RecommenderSystem.DataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor

jsonTools = JsonProcessor()

path = "/Users/george/PycharmProjects/scikitLiterallyLearn/RecommenderSystem/dataFiles/test2.json"

jsonTools = JsonProcessor()

trueData = jsonTools.read_and_sort_data(path)

mockResult = mfa.init_algorithm(trueData)

df = pd.DataFrame(mockResult, columns=['visitorId', 'timestamp', 'transactionPath'])

finalDataFrame = pd.merge(df, trueData, on=['visitorId', 'timestamp'])

finalDataFrame = finalDataFrame.drop(['timestamp', 'pageUrl'], axis=1)
