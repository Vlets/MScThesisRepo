from MasterProject.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from MasterProject.DataAlgorithms.NormalizePersona import NormalizePersona
from MasterProject.DataAlgorithms import UrlKeywordExtractor as urlExtract
import pandas as pd
import numpy as np


class PreprocessingData:

    def __init__(self):
        self.items_table = None
        self.json_tools = JsonProcessor()
        self.list_keywords = None

    def one_hot_encoding_process(self, sortedData):
        """

        :param list_keywords:
        :param sortedData:
        :return:
        """
        keywords_table = self.create_one_hot_encoding_table(self.list_keywords, sortedData, 'keywords')
        sortedData = PreprocessingData.nn_format_pre_process(sortedData)
        sortedData = pd.concat([sortedData, keywords_table], axis=1)
        return sortedData

    def remove_unwanted_rows(self, sorted_data):
        """

        :param sorted_data:
        :return:
        """
        sorted_data['transactionPath'] = sorted_data.transactionPath.apply(self.has_seen_items)
        sorted_data = sorted_data[sorted_data.astype(str)['transactionPath'] != '[]'].reset_index(drop=True)
        return sorted_data

    @staticmethod
    def make_items_table(table):
        """

        :param table:
        :return:
        """
        keep_page_id = ['hst:pages/documentation', 'hst:pages/trail', 'hst:pages/labs-detail']
        keep_columns = ['pageUrl', 'visitorId']
        items_table = table.loc[table['pageId'].isin(keep_page_id)]
        items_table = items_table[keep_columns]
        items_table['keywords'] = items_table.pageUrl.apply(urlExtract.get_keywords, items=True)
        items_table = items_table.drop(columns='visitorId')

        return items_table.drop_duplicates('pageUrl').reset_index(drop=True)

    def create_items_table(self, file_after_processing, file_no_transactions, items_file_name):
        """

        :param file_after_processing:
        :param file_no_transactions:
        :param items_file_name:
        :return:
        """
        table_no_paths = pd.read_json(file_no_transactions).reset_index(drop=True)
        sorted_data = pd.read_json(file_after_processing).reset_index(drop=True)
        items_table = PreprocessingData.make_items_table(table_no_paths)
        list_keywords = self.create_list_all_possible_values(items_table, 'keywords')
        self.items_table = items_table
        self.list_keywords = list_keywords
        items_table.to_json(items_file_name)

        return sorted_data

    @staticmethod
    def create_list_all_possible_values(given_table, column_name):
        """

        :param given_table:
        :param column_name:
        :return:
        """
        values_as_list = [x for x in given_table[column_name].values.tolist() if str(x) != 'nan']
        values = [item for sublist in values_as_list for item in sublist]
        values = sorted(set(values))
        return values

    def has_seen_items(self, path):
        """

        :param path:
        :param items_table:
        :return:
        """
        result = self.items_table.loc[self.items_table['pageUrl'].isin(path)]

        if result.empty:
            return []

        else:
            return path

    @staticmethod
    def create_one_hot_encoding_table(values_list, given_table, column_name):
        """

        :param values_list:
        :param given_table:
        :param column_name:
        :return:
        """
        ohe_table = pd.DataFrame(0, index=np.arange(len(given_table)), columns=values_list)
        i = 0
        visitor_length = len(given_table)
        for index, row in given_table.iterrows():
            values = row[column_name]
            values = [x for x in values if x in values_list]
            ohe_table.loc[index, values] = 1
            i += 1
            if i % 100 == 0:
                print("Progress Table:", round((i / visitor_length) * 100, 2), "%")

        return ohe_table

    @staticmethod
    def nn_format_pre_process(data_to_process):
        """

        :param data_to_process:
        :return:
        """
        result_cities = pd.get_dummies(data_to_process['geo_city'])
        result_cities = result_cities.rename(columns={"": "None_City"})
        result_continent = pd.get_dummies(data_to_process['geo_continent'])
        result_continent = result_continent.rename(columns={"": "None_Continent", "SA": "SA_Continent"})
        result_country = pd.get_dummies(data_to_process['geo_country'])
        result_country = result_country.rename(columns={"": "None_Country"})
        result_persona_id = pd.get_dummies(data_to_process['personaIdScores_id'])
        result_persona_id = result_persona_id.rename(columns={"None": "None_PI"})
        result_global_persona_id = pd.get_dummies(data_to_process['globalPersonaIdScores_id'])
        result_global_persona_id = result_global_persona_id.rename(columns={"None": "None_GPI"})
        users_table = data_to_process.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id',
                                                    'globalPersonaIdScores_id'])
        users_table = pd.concat([users_table,
                                 result_cities, result_continent, result_country,
                                 result_persona_id,
                                 result_global_persona_id
                                 ], axis=1)
        return users_table

    def create_items_table_and_one_hot_encoding(self, no_transactions_file_path, normalized_persona_file_path,
                                                items_file_path, all_data_processed_file_path):
        """

        :param no_transactions_file_path:
        :param normalized_persona_file_path:
        :param items_file_path:
        :param all_data_processed_file_path:
        :return:
        """
        sorted_data = self.create_items_table(normalized_persona_file_path, no_transactions_file_path, items_file_path)
        sorted_data = self.remove_unwanted_rows(sorted_data)
        sorted_data = self.one_hot_encoding_process(sorted_data)
        sorted_data.to_json(all_data_processed_file_path)

    def json_files_pre_process(self, original_data_path, no_transactions_file_path, normalized_personas_file_path):
        """

        :param original_data_path:
        :param no_transactions_file_path:
        :param normalized_personas_file_path:
        :return:
        """
        sorted_data = self.json_tools.json_files_pre_processing(original_data_path, no_transactions_file_path)
        sorted_data = NormalizePersona.normalize_table_personas(sorted_data)
        sorted_data.to_json(normalized_personas_file_path)

    def data_pre_process(self, original_data_path, no_transactions_file_path, normalized_personas_file_path,
                         items_file_path, all_data_processed_file_path):
        """

        :param original_data_path:
        :param no_transactions_file_path:
        :param normalized_personas_file_path:
        :param items_file_path:
        :param all_data_processed_file_path:
        :return:
        """

        self.json_files_pre_process(original_data_path, no_transactions_file_path, normalized_personas_file_path)
        self.create_items_table_and_one_hot_encoding(no_transactions_file_path, normalized_personas_file_path,
                                                     items_file_path, all_data_processed_file_path)