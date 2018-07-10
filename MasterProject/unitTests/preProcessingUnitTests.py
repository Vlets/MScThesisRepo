import unittest
import pandas as pd
import MasterProject.dataFiles.mockData as dataFiles
from MasterProject.DataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from MasterProject.PreprocessingAlgorithms.JsonProcessor import JsonProcessor


# Maximal Forward Reference algorithm will be referred to as: MFA or mfa

class UnitTests(unittest.TestCase):
    jsonTools = JsonProcessor()
    goodData = dataFiles.mockData
    badData = dataFiles.mockData2
    goodReorderedData = dataFiles.mockDataReordered

    def test_MFA_good_data(self):
        processedData = self.process_data(self.goodData)
        result = mfa.init_algorithm(processedData)
        expectedResult = [('1aUserOne',
                           [(1,
                             ['mock.com/home',
                              'mock.com/home/afterhome',
                              'mock.com/home/afterhome/afterafterhome']),
                            (1000, ['mock.com/home', 'mock.com/home/thisshouldbealone'])]),
                          ('2bUserTwo', [(32, ['mock.com/home', 'mock.com/home/afterhome'])]),
                          ('3cUserThree',
                           [(8932,
                             ['mock.com/home/afterhome/afterafterhome',
                              'mock.com/home',
                              'mock.com/home/thisshouldbealone'])])]
        self.assertEqual(result, expectedResult)

    def test_MFA_random_timestamp_data(self):
        processedData = self.process_data(self.badData)
        result = mfa.init_algorithm(processedData)
        expectedResult = [('Annie',
                           [(1, ['mock.com/home', 'mock.com/home/afterhome']),
                            (1000,
                             ['mock.com/home',
                              'mock.com/home/thispageisdifferent',
                              'mock.com/home/afterhome/afterafterhome'])]),
                          ('Smooth Criminal',
                           [(89323,
                             ['mock.com/home/afterhome/afterafterhome',
                              'mock.com/home',
                              'mock.com/home/thispageisdifferent/iswear'])]),
                          ("You've been hit", [(34, ['mock.com/home', 'mock.com/home/afterhome'])]),
                          ('are_you', [(32, ['mock.com/home', 'mock.com/home/afterhome'])]),
                          ('by a', [(10001, ['mock.com/home', 'mock.com/home/thispageisdifferent'])]),
                          ('ok?',
                           [(8932,
                             ['mock.com/home/afterhome/afterafterhome',
                              'mock.com/home',
                              'mock.com/home/thisshouldbealone'])])]
        self.assertEqual(result, expectedResult)

    # reset index makes sure the index numbers do not interfere in the assertion.
    def test_sorting(self):
        result1 = (self.process_data(self.goodData)).reset_index(drop=True)
        result2 = (self.process_data(self.goodReorderedData)).reset_index(drop=True)
        compareDataframes = result1.equals(result2)
        self.assertTrue(compareDataframes)

    # Checks if the length of the resulting list is the same as the number
    # of unique visitorIds in the initial dataFrame.
    def test_did_we_miss_visitors(self):
        sortedData = self.jsonTools.read_and_sort_data(
            "/Users/george/PycharmProjects/scikitLiterallyLearn/MasterProject/dataFiles/test2.json")
        mockResult = mfa.init_algorithm(sortedData)
        self.assertTrue(len(mockResult) == sortedData['visitorId'].nunique())

    def process_data(self, data):
        dataFrame = pd.DataFrame(data)
        sortBy = ["visitorId", "timestamp"]
        sortedData = self.jsonTools.json_sort(dataFrame, sortBy)
        return sortedData


if __name__ == '__main__':
    unittest.main()
