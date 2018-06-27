from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from RecommenderSystem.PreprocessingAlgorithms.ReadingFiles import ReadingFiles as rf
from RecommenderSystem.DataAlgorithms.CalculateSimilarity import CalculateSimilarity as cs
from RecommenderSystem.NeuralNetwork.DNNModel import DNNModel
import pandas as pd

def useless_function(lst1):
    return PreprocessingData.sublist(lst1, predicted_categories)
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
pre_data = PreprocessingData()
dnn_model = DNNModel()

#Process the data
initial_table = pre_data.run_preprocessing("./bloomreach_targeting.json")
visitors = ['3efb952b-21ef-4ebf-b307-cb32ac1eba51']

#Process the data to be acceptable by the DNN
items_table = pre_data.preprocessing_DNN(initial_table, "./processed_bloomreach_targeting.json")
processed_table = pd.read_json("processed_bloomreach_targeting.json")

#Data used to train the DNN
X, Y, X_visitors, Y_visitors, users_table, visitors_table, categories_table, categories_table_visitors, sortedData = \
    dnn_model.preprocess_data(processed_table, visitors)

processed_table = processed_table.reset_index(drop=True)
list_categories = categories_table.columns.values.tolist()

length_x = len(users_table.columns.values.tolist())
length_y = len(list_categories)

dnn_model.create_model(length_x, length_y)

#Training the DNN
results, predictions, accuracy = dnn_model.train_model(X, Y, graphs=True)


visitors_prediction = dnn_model.predict_values(X_visitors)

visitors_prediction[visitors_prediction >= 0.5] = 1
visitors_prediction[visitors_prediction < 0.5] = 0

visitors_accuracy = DNNModel.calculate_accuracy(visitors_prediction, Y_visitors)

#Turn the prediction into table
visitors_prediction_table = pd.DataFrame(visitors_prediction)

#Delete the columns with only 0
result_visitors = visitors_prediction_table.loc[:, (visitors_prediction_table != 0).any(axis=0)]

#Get the indexes of the values in list_categories
indexes = result_visitors.columns.values.tolist()

#Get the actual categories
predicted_categories = [list_categories[x] for x in indexes]

#Get table with items that have the categories found previously
filtered_items = items_table[['pageUrl', 'categories_terms']]
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(useless_function)
filtered_items = filtered_items[filtered_items.astype(str)['categories_terms'] != '[]']
filtered_items = filtered_items.reset_index(drop=True)

#Get visitor past viewed items
visitors_table_path = initial_table.loc[initial_table['visitorId'] == visitors[0]]
list_seen_items = PreprocessingData.create_list(visitors_table_path, 'transactionPath')
list_seen_items = [x for x in list_seen_items if x in items_table.pageUrl.unique().tolist()]
table_seen_items = items_table.loc[items_table['pageUrl'].isin(list_seen_items)][['pageUrl', 'categories_terms']]

#Remove the seen items in filtered_items
table_seen_items = table_seen_items.reset_index(drop=True)
filtered_items = filtered_items.reset_index(drop=True)
filtered_items = filtered_items[(~filtered_items.pageUrl.isin(table_seen_items))]

#Turn categories_terms into strings
filtered_items['categories_terms'] = filtered_items.categories_terms.apply(" ".join)
table_seen_items['categories_terms'] = table_seen_items.categories_terms.apply(" ".join)

#Get list of categories of each item
seen_items_categories = table_seen_items.categories_terms.values.tolist()
filtered_items_categories = filtered_items.categories_terms.values.tolist()
seen_items_names = table_seen_items.pageUrl.values.tolist()
filtered_items_names = filtered_items.pageUrl.values.tolist()
seen_items_tuples = list(zip(seen_items_names, seen_items_categories))
filtered_items_tuples = list(zip(filtered_items_names, filtered_items_categories))

#Calculate similarities
final_result = sorted(cs.similarity_results(seen_items_tuples, filtered_items_tuples))[::-1]
final_result_items = [z for x, y, z in final_result]
final_result_items = PreprocessingData.remove_duplicates(final_result_items)

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

#user_test = initial_table[initial_table['visitorId'] == '022321c9-3447-43f0-8bc7-0a21889328f3']
#visitors = ['022321c9-3447-43f0-8bc7-0a21889328f3']
#initial_table = initial_table.drop([494,495,497,498,499,500,501,502,503,504,505,506,507,508,509,510])
#initial_table = initial_table.reset_index(drop=True)
#aux = processed_table[(processed_table['visitorId'] == visitors[0]) & (processed_table.astype(str)['categories'] != val_to_keep)]
#processed_table = processed_table.drop(aux.index.tolist())
#processed_table = processed_table.reset_index(drop=True)
#actual_seen_items_list = PreprocessingData.create_list(user_test, 'transactionPath')
#actual_seen_items_list = [x for x in actual_seen_items_list if x in items_table.pageUrl.unique().tolist()]
#actual_seen_items_table = items_table.loc[items_table['pageUrl'].isin(actual_seen_items_list)][['pageUrl', 'categories_terms']]
#
#intersection = [x for x in final_result_items if x in actual_seen_items_list]
#indexes = [final_result_items.index(value) for value in intersection]


#percentage_sum = 0
#percentage_result = []
#
#for item in final_result_items:
#    percentage_sum = sum([x for x,y,z in final_result if z == item])
#    percentage_result.append((percentage_sum, item))

