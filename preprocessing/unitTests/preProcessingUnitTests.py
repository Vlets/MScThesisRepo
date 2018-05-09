import unittest
import pandas as pd
import preprocessing.dataFiles.mockData as dataFiles
from preprocessing.Joana.MFAlgorithm import MFAlgorithm as mfa
from preprocessing.helpers.JsonProcessor import JsonProcessor


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
                           [['mock.com/home',
                             'mock.com/home/afterhome',
                             'mock.com/home/afterhome/afterafterhome'],
                            ['mock.com/home', 'mock.com/home/thisshouldbealone']]),
                          ('2bUserTwo', [['mock.com/home', 'mock.com/home/afterhome']]),
                          ('3cUserThree',
                           [['mock.com/home/afterhome/afterafterhome',
                             'mock.com/home',
                             'mock.com/home/thisshouldbealone']])]
        self.assertEqual(result, expectedResult)

    def test_MFA_random_timestamp_data(self):
        processedData = self.process_data(self.badData)
        result = mfa.init_algorithm(processedData)
        expectedResult = [('1aUserOne',
                           [['mock.com/home', 'mock.com/home/afterhome'],
                            ['mock.com/home',
                             'mock.com/home/thisshouldbealone',
                             'mock.com/home/afterhome/afterafterhome']]),
                          ('2bUserTwo', [['mock.com/home', 'mock.com/home/afterhome']]),
                          ('3cUserThree',
                           [['mock.com/home/afterhome/afterafterhome',
                             'mock.com/home',
                             'mock.com/home/thisshouldbealone']])]
        self.assertEqual(result, expectedResult)

    def test_MFA_simple_case(self):
        result = mfa.run_MF_algorithm(['A', 'B', 'C', 'D', 'C', 'B', 'E', 'G', 'H', 'G', 'W', 'A', 'O', 'U', 'O', 'V'])
        expectedResult = [['A', 'B', 'C', 'D'],
                          ['A', 'B', 'E', 'G', 'H'],
                          ['A', 'B', 'E', 'G', 'W'],
                          ['A', 'O', 'U'],
                          ['A', 'O', 'V']]
        self.assertEqual(result, expectedResult)

    # reset index makes sure the index numbers do not interfere in the assertion.
    def test_sorting(self):
        result1 = (self.process_data(self.goodData)).reset_index(drop=True)
        result2 = (self.process_data(self.goodReorderedData)).reset_index(drop=True)
        compareDataframes = result1.equals(result2)
        self.assertTrue(compareDataframes)

    def process_data(self, data):
        dataFrame = pd.DataFrame(data)
        sortBy = ["visitorId", "timestamp"]
        sortedData = self.jsonTools.json_sort(dataFrame, sortBy)
        return sortedData


if __name__ == '__main__':
    unittest.main()
