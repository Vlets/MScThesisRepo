import unittest
import pandas as pd
import segmentation.dataFiles.mockData as dataFiles
from segmentation.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from segmentation.visitorSegmentation.pipelineSteps import VisitorSegmentationPipeline


# Maximal Forward Reference algorithm will be referred to as: MFA or mfa

class UnitTests(unittest.TestCase):
    jsonTools = VisitorSegmentationPipeline()
    goodData = dataFiles.mockData
    badData = dataFiles.mockData2
    goodReorderedData = dataFiles.mockDataReordered

    def test_MFA_good_data(self):
        processed_data = self.process_data(self.goodData)
        result = mfa.init_algorithm(processed_data)
        expected_result = [('1aUserOne',
                            1,
                            ['mock.com/home',
                             'mock.com/home/afterhome',
                             'mock.com/home/afterhome/afterafterhome']),
                           ('1aUserOne', 1000, ['mock.com/home', 'mock.com/home/thisshouldbealone']),
                           ('2bUserTwo', 32, ['mock.com/home', 'mock.com/home/afterhome']),
                           ('3cUserThree',
                            8932,
                            ['mock.com/home/afterhome/afterafterhome',
                             'mock.com/home',
                             'mock.com/home/thisshouldbealone'])]
        self.assertEqual(result, expected_result)

    def test_MFA_random_timestamp_data(self):
        processed_data = self.process_data(self.badData)
        result = mfa.init_algorithm(processed_data)
        expected_result = [('Annie', 1, ['mock.com/home', 'mock.com/home/afterhome']),
                           ('Annie',
                            1000,
                            ['mock.com/home',
                             'mock.com/home/thispageisdifferent',
                             'mock.com/home/afterhome/afterafterhome']),
                           ('Smooth Criminal',
                            89323,
                            ['mock.com/home/afterhome/afterafterhome',
                             'mock.com/home',
                             'mock.com/home/thispageisdifferent/iswear']),
                           ("You've been hit", 34, ['mock.com/home', 'mock.com/home/afterhome']),
                           ('are_you', 32, ['mock.com/home', 'mock.com/home/afterhome']),
                           ('by a', 10001, ['mock.com/home', 'mock.com/home/thispageisdifferent']),
                           ('ok?',
                            8932,
                            ['mock.com/home/afterhome/afterafterhome',
                             'mock.com/home',
                             'mock.com/home/thisshouldbealone'])]
        self.assertEqual(result, expected_result)

    # reset index makes sure the index numbers do not interfere in the assertion.
    def test_sorting(self):
        result1 = (self.process_data(self.goodData)).reset_index(drop=True)
        result2 = (self.process_data(self.goodReorderedData)).reset_index(drop=True)
        compare_data_frames = result1.equals(result2)
        self.assertTrue(compare_data_frames)

    # Checks if the length of the resulting list is the same as the number
    # of unique visitorIds in the initial dataframe.
    def test_did_we_miss_visitors(self):
        path = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
        sorted_data = self.jsonTools.read_and_sort_data(path)
        mock_result = self.jsonTools.get_transactions(sorted_data)
        self.assertTrue(mock_result['visitorId'].nunique() == sorted_data['visitorId'].nunique())

    def process_data(self, data):
        data_frame = pd.DataFrame(data)
        sorted_data = self.jsonTools.json_sort(data_frame)
        return sorted_data


if __name__ == '__main__':
    unittest.main()
