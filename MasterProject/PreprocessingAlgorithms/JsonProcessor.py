import pandas as pd
from MasterProject.DataAlgorithms import UrlKeywordExtractor as urlExtract
from pandas.io.json import json_normalize
from MasterProject.DataAlgorithms.MFAlgorithm import MFAlgorithm as mfa


class JsonProcessor:

    # Step 1
    @staticmethod
    def json_read(filepath, multiline=False):
        file = pd.read_json(filepath, lines=multiline, convert_dates=False)
        return file

    # Step 2
    # Keep list defines all the columns to be kept in the pipeline. All others are dropped.
    @staticmethod
    def filter_columns(data_frame):
        collector_data = json_normalize(data_frame['collectorData'])
        all_data = pd.concat([collector_data, data_frame], axis=1)
        keep_list = ['visitorId', 'timestamp', 'pageUrl', 'geo.country', 'geo.city', 'geo.continent',
                     'globalPersonaIdScores', 'personaIdScores', 'pageId']
        processed_data = all_data[keep_list]
        return processed_data

    # Step 3
    @staticmethod
    def json_sort(file, sort_by):
        if isinstance(sort_by, list):
            sorted_file = file.sort_values(by=sort_by)
            return sorted_file
        raise ValueError("sort_by should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    # Step 4
    def get_transactions(self, sorted_data):
        transactions = mfa.init_algorithm(sorted_data)
        data_frame = pd.DataFrame(transactions, columns=['visitorId', 'timestamp', 'transactionPath'])
        data_frame = pd.merge(data_frame, sorted_data, on=['visitorId', 'timestamp'])

        return data_frame.drop(['timestamp', 'pageUrl'], axis=1)

    # Step 5
    @staticmethod
    def remove_homepage_and_stringify(data_frame):
        transactions = [str(x) for x in data_frame['transactionPath'] if len(x) < 2]
        keep_values = ['hst:pages/productpage']
        result = data_frame[
            (data_frame.astype(str)['transactionPath'].isin(transactions)) & (~data_frame['pageId'].isin(keep_values))]
        indexes = result.index.values.tolist()
        data_frame = data_frame.drop(indexes)
        data_frame = data_frame.reset_index(drop=True)

        return data_frame

    # Steps 1-3 combined
    def read_and_sort_data(self, file_path):
        sort_by = ["visitorId", "timestamp"]
        data_frame = self.json_read(file_path)
        processed_data = self.filter_columns(data_frame)
        sorted_data = self.json_sort(processed_data, sort_by)
        return sorted_data.reset_index(drop=True)

    def json_files_pre_processing(self, file_to_read_path, file_path_to_save):
        """

        :param file_to_read_path:
        :param file_path_to_save:
        :return:
        """
        sorted_data = self.read_and_sort_data(file_to_read_path)
        sorted_data.columns = sorted_data.columns.str.replace("[.]", "_")
        sorted_data.to_json(file_path_to_save)
        final_data_frame = self.get_transactions(sorted_data)
        final_data_frame['keywords'] = final_data_frame.transactionPath.astype(str).apply(urlExtract.get_keywords)
        final_data_frame = self.remove_homepage_and_stringify(final_data_frame)

        return final_data_frame.drop(['pageId'], axis=1)

    @staticmethod
    def json_save(sorted_data, savepath, to_json=True):
        if to_json:
            sorted_data.to_json(savepath + ".json", force_ascii=False)
        if not to_json:
            sorted_data.to_csv(savepath + ".csv")


