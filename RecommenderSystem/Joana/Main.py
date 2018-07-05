from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from RecommenderSystem.PreprocessingAlgorithms.ReadingFiles import ReadingFiles as rf
from RecommenderSystem.DataAlgorithms.CalculateSimilarity import CalculateSimilarity as cs
from RecommenderSystem.NeuralNetwork.DNNModel import DNNModel
import pandas as pd
import numpy as np


# def __init__(self):
#    self.predicted_categories = None

def to_filter_function(lst1):
    ls1 = [element for element in lst1 if element in predicted_categories]
    ls2 = [element for element in predicted_categories if element in lst1]

    if ls1 == ls2:
        return lst1

    else:
        return []


def get_seen_items(table, it_table):
    lst = PreprocessingData.create_list(table, 'transactionPath')
    lst = [x for x in lst if x in it_table.pageUrl.unique().tolist()]
    table_result = it_table.loc[it_table['pageUrl'].isin(lst)][['pageUrl', 'categories_terms']]

    return table_result, lst


url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/processed_bloomreach_targeting_20mb.json"
"""
pre_data = PreprocessingData()


pre_data.run_preprocessing(url, url_no_trans, url_after_everything)

#Process the data to be acceptable by the DNN
pre_data.preprocessing_DNN(url_no_trans, url_after_everything, url_items_file, url_to_save)
"""

initial_table = pd.read_json(url_to_save).reset_index(drop=True)
items_table = pd.read_json(url_items_file).reset_index(drop=True)

list_categories = PreprocessingData.create_list(items_table, 'categories_terms')

dnn_model = DNNModel()
visitor = '2da0f833-c9a8-41fa-86d5-bb179633b87a'  # --> 20mb with no change

user_test = initial_table[initial_table['visitorId'] == '2da0f833-c9a8-41fa-86d5-bb179633b87a']
visitor_indexes = user_test.index.values.tolist()
index_to_drop = visitor_indexes[0]
#user_test = user_test.drop(5574)
#user_test = user_test.drop(2006)
#user_test = user_test.drop(2445)
#visitors = ['0e627f37-3fd8-4b31-93be-a0b2037592fa']
#visitors = ['2da0f833-c9a8-41fa-86d5-bb179633b87a']

#visitor_indexes = [5506, 5514, 5522, 5533, 5542, 5553, 5564, 5596, 5601, 5614, 5622, 5631]
#visitor_indexes = [2007, 2008, 2009, 2010, 2011, 2012, 2014, 2015, 2016, 2017, 2018, 2019]
#visitor_indexes = [2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2459, 2460]


# user_test = user_test.drop(2094) # --> 20mb
# user_test = user_test.drop(1756) # --> 50mb
# user_test = user_test.drop(2090) # --> 30mb
user_test = user_test.drop(index_to_drop)

# visitor_indexes = [2095, 2096, 2097, 2098, 2099, 2100, 2102, 2103, 2104, 2105, 2106, 2107] # --> 20mb
# visitor_indexes = [1759, 1760, 1761, 1762, 1763, 1764, 1765, 1766, 1767, 1769, 1771, 1772] # --> 50mb
# visitor_indexes = [2101, 2113, 2124, 2135, 2157, 2168, 2179, 2190, 2201, 2212, 2225, 2236] # --> 30mb

visitor_indexes.remove(index_to_drop)

actual_seen_items_table, actual_seen_items_list = get_seen_items(user_test, items_table)

initial_table = initial_table.drop(visitor_indexes).reset_index(drop=True)

# Data used to train the DNN
X, Y, X_visitors, Y_visitors, users_table, categories_table, sortedData = \
    dnn_model.preprocess_data(initial_table, user_test, list_categories)

length_x = len(users_table.columns.values.tolist())
length_y = len(categories_table.columns.values.tolist())

dnn_model.create_model(length_x, length_y)

# Training the DNN
dnn_model.train_model(X, Y, graphs=True)

test_value_x = np.array([X_visitors[11].tolist()])
test_value_y = np.array([Y_visitors[11].tolist()])

visitors_prediction = dnn_model.predict_values(test_value_x)
visitors_accuracy = DNNModel.calculate_accuracy(visitors_prediction, test_value_y)

# Turn the prediction into table
visitors_prediction_table = pd.DataFrame(visitors_prediction)

# Delete the columns with only 0
result_visitors = visitors_prediction_table.loc[:, (visitors_prediction_table != 0).any(axis=0)]

# Get the indexes of the values in list_categories
predicted_indexes = result_visitors.columns.values.tolist()

# Get the actual categories
predicted_categories = [list_categories[x] for x in predicted_indexes]
# self.predicted_categories = predicted_categories

# Get table with items that have the categories found previously
filtered_items = items_table.copy()
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(to_filter_function)
filtered_items = filtered_items[filtered_items.astype(str)['categories_terms'] != '[]'].reset_index(drop=True)

# Get visitor past viewed items
visitors_table_path = initial_table.loc[initial_table['visitorId'] == visitor]
table_seen_items, list_seen_items = get_seen_items(visitors_table_path, items_table)
table_seen_items = table_seen_items.reset_index(drop=True)

# Remove the seen items in filtered_items
filtered_items = filtered_items[(~filtered_items.pageUrl.isin(table_seen_items))]

# Turn categories_terms into strings
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(" ".join)
table_seen_items['categories_terms'] = table_seen_items.categories_terms.apply(" ".join)

# Get list of categories of each item
seen_items_categories = table_seen_items.categories_terms.values.tolist()
filtered_items_categories = filtered_items.categories_terms.values.tolist()

# Get list of pageUrls
seen_items_names = table_seen_items.pageUrl.values.tolist()
filtered_items_names = filtered_items.pageUrl.values.tolist()

# Zip the categories and pageUrls
seen_items_tuples = list(zip(seen_items_names, seen_items_categories))
filtered_items_tuples = list(zip(filtered_items_names, filtered_items_categories))

# Calculate similarities
final_result = sorted(cs.similarity_results(seen_items_tuples, filtered_items_tuples))[::-1]
final_result_items = [z for x, y, z in final_result]
final_result_items = PreprocessingData.remove_duplicates(final_result_items)

intersection = [x for x in final_result_items if x in actual_seen_items_list]
indexes = [final_result_items.index(value) for value in intersection]

# count = 0

# for x in indexes:
#    if x < k:
#    count += 1

# return count/k
