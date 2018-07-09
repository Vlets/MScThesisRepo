from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from RecommenderSystem.DataAlgorithms.NormalizePersona import NormalizePersona
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
    def create_list(given_table, column_name):
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

    def useless_function(self, lst1):
        """

        :param lst1:
        :return:
        """
        return PreprocessingData.has_seen_items(lst1, self.items_table)

    @staticmethod
    def create_table(values_list, given_table, column_name):
        """

        :param values_list:
        :param given_table:
        :param column_name:
        :return:
        """
        categories_table = pd.DataFrame(0, index=np.arange(len(given_table)), columns=values_list)
        i = 0
        visitor_length = len(given_table)
        for index, row in given_table.iterrows():
            values = row[column_name]
            values = [x for x in values if x in values_list]
            categories_table.loc[index, values] = 1
            i += 1
            if i % 100 == 0:
                print("Progress Table:", round((i / visitor_length) * 100, 2), "%")

        return categories_table

    def preprocessing_DNN(self, file_no_transactions, file_after_processing, items_file_name, file_path_to_save):
        """

        :param file_no_transactions:
        :param file_after_processing:
        :param items_file_name:
        :param file_path_to_save:
        :return:
        """
        table_no_trans = pd.read_json(file_no_transactions).reset_index(drop=True)
        sortedData = pd.read_json(file_after_processing).reset_index(drop=True)
        items_table = JsonProcessor.make_items_table(table_no_trans)
        self.items_table = items_table
        items_table.to_json(items_file_name)
        list_categories = self.create_list(items_table, 'categories_terms')
        sortedData['transactionPath'] = sortedData.transactionPath.apply(self.useless_function)
        sortedData = sortedData[sortedData.astype(str)['transactionPath'] != '[]'].reset_index(drop=True)
        categories_table = self.create_table(list_categories, sortedData, 'categories')
        sortedData = pd.concat([sortedData, categories_table], axis=1)
        # sortedData = sortedData.drop(columns=['transactionPath'])
        sortedData.to_json(file_path_to_save)

    def run_preprocessing(self, name_file, file_to_save, file_after_everything):
        """

        :param name_file:
        :param file_to_save:
        :param file_after_everything:
        :return:
        """
        sortedData = self.json_tools.do_it_all(name_file, file_to_save)
        sortedData = NormalizePersona.normalize_table_personas(sortedData)
        sortedData.to_json(file_after_everything)
