from preprocessing.helpers.ReadingFiles import ReadingFiles as rf
from preprocessing.dataAlgorithms.CalculateSimilarity import CalculateSimilarity as cs
from preprocessing.helpers.PreprocessingData import PreprocessingData
from preprocessing.Joana.DNNModel import DNNModel
import pandas as pd


def useless_function(lst1):
    return PreprocessingData.sublist(lst1, predicted_categories)

"""uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

reading_files = rf()
reading_files.connect_to_database(uri)

#Choose the amount of data to work with
query = 'SELECT entry FROM requestlog LIMIT 91824'

#Process the json data and save into a file
query_result = reading_files.make_query(query)
reading_files.query_to_json_file(query_result, 'entry',
                                 "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/preprocessing/Joana"
                                 "/bloomreach_targeting.json")

"""
pre_data = PreprocessingData()
dnn_model = DNNModel()

#Process the data
initial_table = pre_data.run_preprocessing("./bloomreach_targeting.json")
visitors = ['3efb952b-21ef-4ebf-b307-cb32ac1eba51']

#Process the data to be acceptable by the DNN
items_table = pre_data.preprocessing_DNN(initial_table, "./processed_bloomreach_targeting.json")

#Data used to train the DNN
X, Y, X_visitors, Y_visitors, users_table, visitors_table, categories_table, categories_table_visitors, sortedData = \
    dnn_model.preprocess_data("processed_bloomreach_targeting.json", visitors)

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
