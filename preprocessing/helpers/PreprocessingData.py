from preprocessing.helpers.JsonProcessor import JsonProcessor
from preprocessing.dataAlgorithms.NormalizePersona import NormalizePersona
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
    def create_categories_list(items_table, word):
        if word == 'categories_terms':
            list_categories = [x for x in items_table.categories_terms.values.tolist() if str(x) != 'nan']
        elif word == 'categories':
            list_categories = [x for x in items_table.categories.values.tolist() if str(x) != 'nan']
        categories = [item for sublist in list_categories for item in sublist]
        categories = PreprocessingData.remove_duplicates(categories)
        return categories

    @staticmethod
    def create_audience_list(items_table):
        list_audience = [x for x in items_table.audience_terms.values.tolist() if str(x) != 'nan']
        audience = [item for sublist in list_audience for item in sublist]
        audience = PreprocessingData.remove_duplicates(audience)
        return audience

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
        list_categories = self.create_categories_list(items_table, 'categories_terms')
        self.list_categories = list_categories
        sortedData = sortedData[pd.notna(sortedData['categories'])]
        sortedData = sortedData.reset_index(drop=True)
        sortedData['categories'] = sortedData.categories.apply(self.useless_function)
        sortedData = sortedData[sortedData.astype(str)['categories'] != '[]']
        sortedData = sortedData.reset_index(drop=True)
        categories_table = self.create_table(list_categories, sortedData, 'categories')
        list_audience = self.create_audience_list(items_table)
        self.list_audience = list_audience
        audience_table = self.create_table(list_audience, sortedData, 'audience_terms')
        sortedData = sortedData.drop(columns=['transactionPath', 'visitorId', 'userAgent'])
        sortedData = pd.concat([sortedData, audience_table, categories_table], axis=1)
        sortedData = sortedData.drop(columns=['audience_terms'])
        sortedData.to_json(file_name)

    def run_preprocessing(self, name_file):

        sortedData = self.json_tools.do_it_all(name_file)
        # sortedData = json_Tools.do_it_all("./test_mb.json")
        # sortedData.to_json("./test2_processed.json")

        # sortedData = pd.read_json("./test2_processed_personas.json")
        # sortedData = sortedData.reset_index(drop=True)
        # sortedData = sortedData.drop(columns=['referer', 'audience.terms', 'categories.terms', 'userAgent', 'visitorId'])

        sortedData = NormalizePersona.normalize_table_personas(sortedData)
        # sortedData.to_json("./test2_processed_personas.json")

        # sortedData = pd.read_json("./test2_processed_personas.json")
        # sortedData = sortedData.reset_index(drop=True)

        return sortedData