import pandas as pd
import preprocessing.dataFiles.mockData as dataFiles
from preprocessing.Joana.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.helpers.JsonProcessor import JsonProcessor
import time

dataFrameMock = pd.DataFrame(dataFiles.mockData)
dataFrameMock2 = pd.DataFrame(dataFiles.mockData2)

jsonTools = JsonProcessor()

sortedData = jsonTools.json_sort(dataFrameMock2, ['visitorId', 'timestamp'])

mockResult = mfa.init_algorithm(sortedData)

df = pd.DataFrame(mockResult, columns=['visitorId', 'transaction'])

lst = df['transaction'].tolist()
tlist = pd.DataFrame(lst[0], columns=['timestamp', 'path'])

for x in range(1, len(lst)):
    temp = pd.DataFrame(lst[x], columns=['timestamp', 'path'])
    tlist = pd.concat([tlist, temp], join='outer', axis=0)