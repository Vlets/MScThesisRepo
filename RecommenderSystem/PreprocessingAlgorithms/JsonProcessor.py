import pandas as pd
from pandas.io.json import json_normalize
from RecommenderSystem.DataAlgorithms.MFAlgorithm import MFAlgorithm as mfa


class JsonProcessor:

    def __init__(self):
        self.file = None
        self.list_pageid = []

    @staticmethod
    def json_read(filepath, multiline=False):
        file = pd.read_json(filepath, lines=multiline, convert_dates=False)
        return file

    @staticmethod
    def json_sort(file, sort_by):
        if isinstance(sort_by, list):
            sorted_file = file.sort_values(by=sort_by)
            return sorted_file
        raise ValueError("sort_by should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    @staticmethod
    def normalize_collectors(data_frame):
        collector_data = json_normalize(data_frame['collectorData'])
        all_data = pd.concat([collector_data, data_frame], axis=1)
        keep_list = ['visitorId', 'timestamp', 'pageUrl', 'geo.country', 'geo.city', 'geo.continent', 'audience.terms',
                     'categories.terms', 'globalPersonaIdScores', 'personaIdScores', 'pageId']
        processed_data = all_data[keep_list]
        print("Step 2/6 - Filtering, done...")
        return processed_data

    def make_items_table(self):
        table = self.file
        keep_values = ['hst:pages/documentation', 'hst:pages/trail', 'hst:pages/labs-detail']
        keep_columns = ['pageUrl', 'audience_terms', 'categories_terms']
        items_table = table.loc[table['pageId'].isin(keep_values)]
        items_table = items_table[keep_columns]
        return items_table.drop_duplicates('pageUrl').reset_index(drop=True)

    def read_and_sort_data(self, file_path):
        sort_by = ["visitorId", "timestamp"]
        data_frame = self.json_read(file_path)
        processed_data = self.normalize_collectors(data_frame)
        sorted_data = self.json_sort(processed_data, sort_by)
        return sorted_data.reset_index(drop=True)

    def do_it_all(self, file_path):
        sorted_data = self.read_and_sort_data(file_path)
        sorted_data.columns = sorted_data.columns.str.replace("[.]", "_")
        self.file = sorted_data
        self.list_pageid = mfa.remove_duplicates(sorted_data.pageId.tolist())
        transactions = mfa.init_algorithm(sorted_data)
        transaction_dataframe = pd.DataFrame(transactions,
                                             columns=['visitorId', 'timestamp', 'transactionPath', 'categories'])
        final_data_frame = pd.merge(transaction_dataframe, sorted_data, on=['visitorId', 'timestamp'])
        return final_data_frame.drop(['timestamp', 'pageUrl', 'categories_terms', 'pageId'], axis=1)

    @staticmethod
    def json_save(sorted_data, savepath, to_json=True):
        if to_json:
            sorted_data.to_json(savepath + ".json", force_ascii=False)
        if not to_json:
            sorted_data.to_csv(savepath + ".csv")


