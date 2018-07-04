from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from RecommenderSystem.DataAlgorithms.NormalizePersona import NormalizePersona
import pandas as pd
import numpy as np


class PreprocessingData:

    def __init__(self):
        self.items_table = None
        self.list_categories = None
        self.list_audience = None
        self.json_tools = JsonProcessor()

    @staticmethod
    def remove_duplicates(duplicate):
        final_list = []
        for num in duplicate:
            if num not in final_list:
                final_list.append(num)
        return final_list

    @staticmethod
    def create_list(items_table, word):
        list_categories = [x for x in items_table[word].values.tolist() if str(x) != 'nan']
        categories = [item for sublist in list_categories for item in sublist]
        categories = PreprocessingData.remove_duplicates(categories)
        return categories

    @staticmethod
    def has_seen_items(path, items_table):
        result = items_table.loc[items_table['pageUrl'].isin(path)]

        if result.empty:
            return []

        else:
            return path

    def useless_function(self, lst1):
        return PreprocessingData.has_seen_items(lst1, self.items_table)

    @staticmethod
    def create_table(list_categories, items_table, column):
        categories_table = pd.DataFrame(0, index=np.arange(len(items_table)), columns=list_categories)
        i = 0
        visitor_length = len(items_table)
        for index, row in items_table.iterrows():
            values = row[column]
            values = [x for x in values if x in list_categories]
            categories_table.loc[index, values] = 1
            i += 1
            if i % 100 == 0:
                print("Progress Table:", round((i / visitor_length) * 100, 2), "%")

        return categories_table

    def preprocessing_DNN(self, file_no_trans, file_after_everything, items_file_name, file_name,):

        table_no_trans = pd.read_json(file_no_trans).reset_index(drop=True)
        sortedData = pd.read_json(file_after_everything).reset_index(drop=True)
        items_table = JsonProcessor.make_items_table(table_no_trans)
        self.items_table = items_table
        items_table.to_json(items_file_name)
        list_categories = self.create_list(items_table, 'categories_terms')
        self.list_categories = list_categories
        sortedData['transactionPath'] = sortedData.transactionPath.apply(self.useless_function)
        sortedData = sortedData[sortedData.astype(str)['transactionPath'] != '[]'].reset_index(drop=True)
        categories_table = self.create_table(list_categories, sortedData, 'categories')
        sortedData = pd.concat([sortedData, categories_table], axis=1)
        #sortedData = sortedData.drop(columns=['transactionPath'])
        sortedData.to_json(file_name)



    def run_preprocessing(self, name_file, file_to_save, file_after_everything):

        sortedData = self.json_tools.do_it_all(name_file, file_to_save)
        sortedData = NormalizePersona.normalize_table_personas(sortedData)
        sortedData.to_json(file_after_everything)

