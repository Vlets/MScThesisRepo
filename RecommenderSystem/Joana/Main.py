from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from RecommenderSystem.PreprocessingAlgorithms.ReadingFiles import ReadingFiles as rf
from RecommenderSystem.DataAlgorithms.CalculateSimilarity import CalculateSimilarity as cs
from RecommenderSystem.NeuralNetwork.DNNModel import DNNModel
import pandas as pd
import numpy as np

<<<<<<< HEAD
"""
uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

reading_files = rf()
reading_files.connect_to_database(uri)

#Choose the amount of data to work with
query = 'SELECT entry FROM requestlog LIMIT 99824'

#Process the json data and save into a file
query_result = reading_files.make_query(query)
reading_files.query_to_json_file(query_result, 'entry',
                                 "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/Joana"
                                 "/bloomreach_targeting.json")

"""


def to_filter_function(lst1):
    #return PreprocessingData.sublist(lst1, predicted_categories)
=======
def useless_function(lst1):
    value = 0
>>>>>>> parent of 95ddc26... Refactoring

    for x in lst1:
        if x in predicted_categories:
            value = 1

<<<<<<< HEAD
    if ls1 == ls2 and ls1 != []:
=======
    if value == 1:
>>>>>>> parent of 95ddc26... Refactoring
        return lst1

    else:
        return []

<<<<<<< HEAD
    # value = 0

    # for x in lst1:
    #    if x in predicted_categories:
    #        value = 1

    # if value == 1:
    #    return lst1

    # else:
    #    return []

=======
"""
uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

reading_files = rf()
reading_files.connect_to_database(uri)

#Choose the amount of data to work with
query = 'SELECT entry FROM requestlog LIMIT 99824'
>>>>>>> parent of 95ddc26... Refactoring

pre_data = PreprocessingData()
dnn_model = DNNModel()

<<<<<<< HEAD
# Process the data
url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/processed_bloomreach_targeting_20mb.json"
=======
#user_test = initial_table[initial_table['visitorId'] == '022321c9-3447-43f0-8bc7-0a21889328f3']
#visitors = ['022321c9-3447-43f0-8bc7-0a21889328f3']
#val_to_keep = user_test.categories.loc[496]
#val_to_keep = str(val_to_keep)
#initial_table = initial_table.drop([494,495,497,498,499,500,501,502,503,504,505,506,507,508,509,510])
#initial_table = initial_table.reset_index(drop=True)
#aux = processed_table[(processed_table['visitorId'] == visitors[0]) & (processed_table.astype(str)['categories'] != val_to_keep)]
#processed_table = processed_table.drop(aux.index.tolist())
#processed_table = processed_table.reset_index(drop=True)
#actual_seen_items_list = PreprocessingData.create_list(user_test, 'transactionPath')
#actual_seen_items_list = [x for x in actual_seen_items_list if x in items_table.pageUrl.unique().tolist()]
#actual_seen_items_table = items_table.loc[items_table['pageUrl'].isin(actual_seen_items_list)][['pageUrl', 'categories_terms']]
#


#trans = [x for x in initial_table['transactionPath'] if len(ast.literal_eval(x)) < 2]
#keep_values = ['hst:pages/documentation', 'hst:pages/trail', 'hst:pages/labs-detail']
#result = initial_table[(initial_table.transactionPath.isin(trans))  & (~initial_table['pageId'].isin(keep_values))]
#indexes = result.index.values.tolist()
#initial_table = initial_table.drop(indexes)
#initial_table = initial_table.reset_index(drop=True)


#Process the data
url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_50mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_no_transactions_50mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_everything_50mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_items_50mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/processed_bloomreach_targeting_50mb.json"
>>>>>>> parent of 95ddc26... Refactoring
"""
pre_data.run_preprocessing(url, url_no_trans, url_after_everything)

#Process the data to be acceptable by the DNN
pre_data.preprocessing_DNN(url_no_trans, url_after_everything, url_items_file, url_to_save)
"""

initial_table = pd.read_json(url_to_save).reset_index(drop=True)
items_table = pd.read_json(url_items_file).reset_index(drop=True)

<<<<<<< HEAD
list_categories = PreprocessingData.create_list(items_table, 'categories_terms')

user_test = initial_table[initial_table['visitorId'] == '2da0f833-c9a8-41fa-86d5-bb179633b87a']
# user_test = user_test.drop(5574)
# user_test = user_test.drop(2006) # --> 20mb
user_test = user_test.drop(2094) # --> 20mb with change
# user_test = user_test.drop(1756) # --> 50mb
# user_test = user_test.drop(2090) # --> 30mb
# user_test = user_test.drop(2445)
visitor = '2da0f833-c9a8-41fa-86d5-bb179633b87a' # --> 20mb with no change

# visitor_indexes = [5506, 5514, 5522, 5533, 5542, 5553, 5564, 5596, 5601, 5614, 5622, 5631]
# visitor_indexes = [2007, 2008, 2009, 2010, 2011, 2012, 2014, 2015, 2016, 2017, 2018, 2019] # --> 20mb
visitor_indexes = [2095, 2096, 2097, 2098, 2099, 2100, 2102, 2103, 2104, 2105, 2106, 2107] # --> 20mb with change
# visitor_indexes = [1759, 1760, 1761, 1762, 1763, 1764, 1765, 1766, 1767, 1769, 1771, 1772] # --> 50mb
# visitor_indexes = [2101, 2113, 2124, 2135, 2157, 2168, 2179, 2190, 2201, 2212, 2225, 2236] # --> 30mb
# visitor_indexes = [2448, 2449, 2450, 2451, 2452, 2453, 2454, 2455, 2456, 2457, 2459, 2460]
=======
user_test = initial_table[initial_table['visitorId'] == '0e627f37-3fd8-4b31-93be-a0b2037592fa']
#visitors = ['3efb952b-21ef-4ebf-b307-cb32ac1eba51']
#visitors = ['022321c9-3447-43f0-8bc7-0a21889328f3']
#visitors = ['05c457ab-9050-487f-a617-748ef8b3ed9c']
#visitors = ['11bfd688-535a-4f63-9a6f-180bbca91cbe']
visitors = ['0e627f37-3fd8-4b31-93be-a0b2037592fa']

visitors_indexes = [5506, 5514, 5522, 5533, 5542, 5553, 5564, 5596, 5601, 5614, 5622, 5631]
>>>>>>> parent of 95ddc26... Refactoring

actual_seen_items_list = PreprocessingData.create_list(user_test, 'transactionPath')
actual_seen_items_list = [x for x in actual_seen_items_list if x in items_table.pageUrl.unique().tolist()]
actual_seen_items_table = items_table.loc[items_table['pageUrl'].isin(actual_seen_items_list)][
    ['pageUrl', 'categories_terms']]

<<<<<<< HEAD
initial_table = initial_table.drop(visitor_indexes)
initial_table = initial_table.reset_index(drop=True)

# Data used to train the DNN
X, Y, X_visitors, Y_visitors, users_table, categories_table, sortedData = \
    dnn_model.preprocess_data(initial_table, user_test, list_categories)

=======
val_to_keep = initial_table.transactionPath.loc[5574]
#val_to_keep = initial_table.categories.loc[90]
#val_to_keep = initial_table.transactionPath.loc[162]
val_to_keep = str(val_to_keep)

initial_table = initial_table.drop(visitors_indexes)
#initial_table = initial_table.drop([91])
#initial_table = initial_table.drop([154, 155, 156, 157, 158, 159, 160, 161, 163, 164, 165, 166])
initial_table = initial_table.reset_index(drop=True)

#pre_data.preprocessing_DNN(user_test, "./processed_user_test.json")
#processed_table = pd.read_json("processed_bloomreach_targeting.json")
#processed_table_test = pd.read_json("processed_user_test.json")

#Data used to train the DNN
X, Y, X_visitors, Y_visitors, users_table, visitors_table, categories_table, categories_table_visitors, sortedData = \
    dnn_model.preprocess_data(url_to_save, visitors, val_to_keep)
#X_test, Y_test, X_visitors_test, Y_visitors_test, users_table_test, visitors_table_test, categories_table_test, categories_table_visitors_test, sortedData_test = \
#    dnn_model.preprocess_data(processed_table_test, [])


#processed_table = processed_table.reset_index(drop=True)
list_categories = categories_table.columns.values.tolist()

>>>>>>> parent of 95ddc26... Refactoring
length_x = len(users_table.columns.values.tolist())
length_y = len(list_categories)

dnn_model.create_model(length_x, length_y)

<<<<<<< HEAD
# Training the DNN
dnn_model.train_model(X, Y, graphs=True)
=======

#Training the DNN
results, predictions, accuracy = dnn_model.train_model(X, Y, graphs=True)
>>>>>>> parent of 95ddc26... Refactoring

test_value_x = X_visitors[11]
test_value_x = [test_value_x.tolist()]
test_value_x = np.array(test_value_x)

test_value_y = Y_visitors[11]
test_value_y = [test_value_y.tolist()]
test_value_y = np.array(test_value_y)

visitors_prediction = dnn_model.predict_values(test_value_x)

visitors_prediction[visitors_prediction >= 0.5] = 1
visitors_prediction[visitors_prediction < 0.5] = 0

visitors_accuracy = DNNModel.calculate_accuracy(visitors_prediction, test_value_y)

# Turn the prediction into table
visitors_prediction_table = pd.DataFrame(visitors_prediction)

# Delete the columns with only 0
result_visitors = visitors_prediction_table.loc[:, (visitors_prediction_table != 0).any(axis=0)]

# Get the indexes of the values in list_categories
predicted_indexes = result_visitors.columns.values.tolist()

# Get the actual categories
predicted_categories = [list_categories[x] for x in predicted_indexes]

<<<<<<< HEAD
# Get table with items that have the categories found previously
filtered_items = items_table
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(to_filter_function)
=======
#Get table with items that have the categories found previously
filtered_items = items_table[['pageUrl', 'categories_terms']]
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(useless_function)
>>>>>>> parent of 95ddc26... Refactoring
filtered_items = filtered_items[filtered_items.astype(str)['categories_terms'] != '[]']
filtered_items = filtered_items.reset_index(drop=True)

# Get visitor past viewed items
visitors_table_path = initial_table.loc[initial_table['visitorId'] == visitor]
list_seen_items = PreprocessingData.create_list(visitors_table_path, 'transactionPath')
list_seen_items = [x for x in list_seen_items if x in items_table.pageUrl.unique().tolist()]
table_seen_items = items_table.loc[items_table['pageUrl'].isin(list_seen_items)][['pageUrl', 'categories_terms']]

# Remove the seen items in filtered_items
table_seen_items = table_seen_items.reset_index(drop=True)
filtered_items = filtered_items.reset_index(drop=True)
filtered_items = filtered_items[(~filtered_items.pageUrl.isin(table_seen_items))]

# Turn categories_terms into strings
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(" ".join)
table_seen_items['categories_terms'] = table_seen_items.categories_terms.apply(" ".join)

# Get list of categories of each item
seen_items_categories = table_seen_items.categories_terms.values.tolist()
filtered_items_categories = filtered_items.categories_terms.values.tolist()
<<<<<<< HEAD

# Get list of pageUrls
seen_items_names = table_seen_items.pageUrl.values.tolist()
filtered_items_names = filtered_items.pageUrl.values.tolist()

# Zip the categories and pageUrls
=======
seen_items_names = table_seen_items.pageUrl.values.tolist()
filtered_items_names = filtered_items.pageUrl.values.tolist()
>>>>>>> parent of 95ddc26... Refactoring
seen_items_tuples = list(zip(seen_items_names, seen_items_categories))
filtered_items_tuples = list(zip(filtered_items_names, filtered_items_categories))

# Calculate similarities
final_result = sorted(cs.similarity_results(seen_items_tuples, filtered_items_tuples))[::-1]
final_result_items = [z for x, y, z in final_result]
final_result_items = PreprocessingData.remove_duplicates(final_result_items)

intersection = [x for x in final_result_items if x in actual_seen_items_list]
indexes = [final_result_items.index(value) for value in intersection]
<<<<<<< HEAD
=======

#When testing with only one trasactionPath
#test_value = visitors_table.loc[5].values.tolist()
#test_value = [test_value]
#test_value = np.array(test_value)
#result_test_value = dnn_model.predict_values(test_value)
#
#result_test_value[result_test_value >= 0.5] = 1
#result_test_value[result_test_value < 0.5] = 0
#
#test_value_y = categories_table_visitors.iloc[5].values.tolist()
#test_value_y = [test_value_y]
#test_value_y = np.array(test_value_y)
#
#
# '022321c9-3447-43f0-8bc7-0a21889328f3'
# 494 - 510 --> 497


#percentage_sum = 0
#percentage_result = []
#
#for item in final_result_items:
#    percentage_sum = sum([x for x,y,z in final_result if z == item])
#    percentage_result.append((percentage_sum, item))
>>>>>>> parent of 95ddc26... Refactoring
