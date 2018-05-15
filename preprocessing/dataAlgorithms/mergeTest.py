import pandas as pd
import preprocessing.dataFiles.mockData as dataFiles
from preprocessing.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.helpers.JsonProcessor import JsonProcessor

jsonTools = JsonProcessor()

path = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"

jsonTools = JsonProcessor()

trueData = jsonTools.read_and_sort_data(path)

mockResult = mfa.init_algorithm(trueData)

df = pd.DataFrame(mockResult, columns=['visitorId', 'timestamp', 'transactionPath'])

finalDataFrame = pd.merge(df, trueData, on=['visitorId', 'timestamp'])

finalDataFrame = finalDataFrame.drop(['timestamp', 'pageUrl'], axis=1)
