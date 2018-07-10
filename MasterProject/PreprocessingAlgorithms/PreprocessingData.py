from MasterProject.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from MasterProject.DataAlgorithms.NormalizePersona import NormalizePersona
import pandas as pd
import numpy as np


class PreprocessingData:

    def __init__(self):
        self.items_table = None
        self.json_tools = JsonProcessor()

    @staticmethod
    def remove_duplicates(duplicate):
        final_list = []
        for num in duplicate:
            if num not in final_list:
                final_list.append(num)
        return final_list

    @staticmethod
    def NN_format_preprocess(data_to_process):
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

    def one_hot_encoding_process(self, list_keywords, sortedData):
        keywords_table = self.create_one_hot_encoding_table(list_keywords, sortedData, 'keywords')
        sortedData = PreprocessingData.NN_format_preprocess(sortedData)
        sortedData = pd.concat([sortedData, keywords_table], axis=1)
        return sortedData

    def remove_unwanted_rows(self, sortedData):
        sortedData['transactionPath'] = sortedData.transactionPath.apply(self.to_apply_has_seen_items_function)
        sortedData = sortedData[sortedData.astype(str)['transactionPath'] != '[]'].reset_index(drop=True)
        return sortedData

    def create_items_table(self, file_after_processing, file_no_transactions, items_file_name):
        table_no_paths = pd.read_json(file_no_transactions).reset_index(drop=True)
        sortedData = pd.read_json(file_after_processing).reset_index(drop=True)
        items_table = JsonProcessor.make_items_table(table_no_paths)
        self.items_table = items_table
        items_table.to_json(items_file_name)

        return items_table, sortedData

    @staticmethod
    def create_list_all_possible_values(given_table, column_name):
        """

        :param given_table:
        :param column_name:
        :return:
        """
        values_as_list = [x for x in given_table[column_name].values.tolist() if str(x) != 'nan']
        values = [item for sublist in values_as_list for item in sublist]
        values = PreprocessingData.remove_duplicates(values)
        return values

    @staticmethod
    def has_seen_items(path, items_table):
        """

        :param path:
        :param items_table:
        :return:
        """
        result = items_table.loc[items_table['pageUrl'].isin(path)]

        if result.empty:
            return []

        else:
            return path

    def to_apply_has_seen_items_function(self, lst1):
        """

        :param lst1:
        :return:
        """
        return PreprocessingData.has_seen_items(lst1, self.items_table)

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

    def create_items_table_and_one_hot_encoding(self, file_no_transactions, file_after_processing, items_file_name,
                                                file_path_to_save):
        """

        :param file_no_transactions:
        :param file_after_processing:
        :param items_file_name:
        :param file_path_to_save:
        :return:
        """
        items_table, sortedData = self.create_items_table(file_after_processing, file_no_transactions, items_file_name)
        list_keywords = self.create_list_all_possible_values(items_table, 'keywords')
        sortedData = self.remove_unwanted_rows(sortedData)
        sortedData = self.one_hot_encoding_process(list_keywords, sortedData)
        sortedData.to_json(file_path_to_save)

    def json_files_pre_process(self, name_file, file_to_save, file_after_everything):
        """

        :param name_file:
        :param file_to_save:
        :param file_after_everything:
        :return:
        """
        sortedData = self.json_tools.json_files_pre_processing(name_file, file_to_save)
        sortedData = NormalizePersona.normalize_table_personas(sortedData)
        sortedData.to_json(file_after_everything)

