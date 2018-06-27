from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from RecommenderSystem.DataAlgorithms.NormalizePersona import NormalizePersona
import pandas as pd
import numpy as np


class PreprocessingData:

    def __init__(self):
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
    def sublist(lst1, lst2):
        ls1 = [element for element in lst1 if element in lst2]

        if len(ls1) == len(lst1):
            return lst1
        else:
            return []

    def useless_function(self, lst1):
        return PreprocessingData.sublist(lst1, self.list_categories)

    @staticmethod
    def create_table(list_categories, items_table, column):
        categories_table = pd.DataFrame(0, index=np.arange(len(items_table)), columns=list_categories)
        i = 0
        visitor_length = len(items_table)
        for index, row in items_table.iterrows():
            values = row[column]
            categories_table.loc[index, values] = 1
            i += 1
            if i % 100 == 0:
                print("Progress:", round((i / visitor_length) * 100, 2), "%")

        return categories_table

    def preprocessing_DNN(self, sortedData, file_name):

        items_table = self.json_tools.make_items_table()
        items_table = items_table[pd.notna(items_table['categories_terms'])]
        items_table = items_table[items_table.astype(str)['categories_terms'] != '[\'\']']
        items_table = items_table.reset_index(drop=True)
        list_categories = self.create_list(items_table, 'categories_terms')
        self.list_categories = list_categories
        sortedData = sortedData[pd.notna(sortedData['categories'])]
        sortedData = sortedData.reset_index(drop=True)
        sortedData['categories'] = sortedData.categories.apply(self.useless_function)
        sortedData = sortedData[sortedData.astype(str)['categories'] != '[]']
        sortedData = sortedData.reset_index(drop=True)
        categories_table = self.create_table(list_categories, sortedData, 'categories')
        list_audience = self.create_list(items_table, 'audience_terms')
        self.list_audience = list_audience
        audience_table = self.create_table(list_audience, sortedData, 'audience_terms')
        sortedData = pd.concat([sortedData, audience_table, categories_table], axis=1)
        sortedData = sortedData.drop(columns=['transactionPath', 'audience_terms'])
        sortedData.to_json(file_name)

        return items_table


    def run_preprocessing(self, name_file):

        sortedData = self.json_tools.do_it_all(name_file)
        sortedData = NormalizePersona.normalize_table_personas(sortedData)

        return sortedData