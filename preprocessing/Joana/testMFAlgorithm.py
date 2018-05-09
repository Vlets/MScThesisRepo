import pandas as pd
import numpy as np

from preprocessing.Joana.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.JsonProcessor import JsonProcessor

test = mfa.run_MF_algorithm(['A', 'B', 'C', 'D', 'C', 'B', 'E', 'G', 'H', 'G', 'W', 'A', 'O', 'U', 'O', 'V'])

mockData = [{'visitorId': '1', 'pageUrl': 'mock.com/home', 'timestamp': '1'},
            {'visitorId': '1', 'pageUrl': 'mock.com/home/afterhome', 'timestamp': '3'},
            {'visitorId': '1', 'pageUrl': 'mock.com/home/afterhome/afterafterhome', 'timestamp': '5'},
            {'visitorId': '1', 'pageUrl': 'mock.com/home', 'timestamp': '7'},
            {'visitorId': '1', 'pageUrl': 'mock.com/home/thisshouldbealone', 'timestamp': '9'},
            {'visitorId': '2', 'pageUrl': 'mock.com/home', 'timestamp': '1'},
            {'visitorId': '2', 'pageUrl': 'mock.com/home/afterhome', 'timestamp': '3'},
            {'visitorId': '3', 'pageUrl': 'mock.com/home/afterhome/afterafterhome', 'timestamp': '5'},
            {'visitorId': '3', 'pageUrl': 'mock.com/home', 'timestamp': '7'},
            {'visitorId': '3', 'pageUrl': 'mock.com/home/thisshouldbealone', 'timestamp': '9'}]

dataFrame = pd.DataFrame(mockData)

#Test the algorithm with actual data
jsonTools = JsonProcessor()

#dataFrame = jsonTools.json_read("/Users/Joana/Documents/GitHub/scikitLiterallyLearn/preprocessing/Joana/test2.json")

sortBy = ["visitorId", "timestamp"]
sortedData = jsonTools.json_sort(dataFrame, sortBy)

visitors = sortedData.visitorId.unique()

paths = []

for visitor in visitors:
    path = []
    dataResult = sortedData.loc[sortedData['visitorId'] == visitor]
    urls = dataResult.pageUrl
    for url in urls:
        path.append(url)
    paths.append((visitor, path))

result = []
for elem in paths:
    visitor, path = elem
    for url in path:
        index = path.index(url)
        url += '|'
        path[index] = url
    resultingPath = mfa.run_MF_algorithm(path)
    resultPaths = []
    for reference in resultingPath:
        resultPaths.append(reference.split('|')[:-1])
    result.append((visitor, resultPaths))

