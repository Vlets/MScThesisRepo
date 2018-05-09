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

dataFrameMock = pd.DataFrame(mockData)

jsonTools = JsonProcessor()
#dataFrame = jsonTools.json_read("/Users/Joana/Documents/GitHub/scikitLiterallyLearn/preprocessing/Joana/test2.json")
dataFrame2 = jsonTools.json_read("/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/testProduced.json")

sortBy = ["visitorId", "timestamp"]
sortedData = jsonTools.json_sort(dataFrame2, sortBy)

result = mfa.init_algorithm(sortedData)



