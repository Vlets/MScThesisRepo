from preprocessing.helpers.ReadingFiles import ReadingFiles as rf
from preprocessing.helpers.PreprocessingData import PreprocessingData
from preprocessing.Joana.DNNModel import DNNModel

"""uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

reading_files = rf()
reading_files.connect_to_database(uri)

query = 'SELECT entry FROM requestlog LIMIT 45912'

query_result = reading_files.make_query(query)
reading_files.query_to_json_file(query_result, 'entry',
                                 "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/preprocessing/Joana"
                                 "/bloomreach_targeting.json")

"""
pre_data = PreprocessingData()
dnn_model = DNNModel()

initial_table = pre_data.run_preprocessing("./bloomreach_targeting.json")
visitor = '3efb952b-21ef-4ebf-b307-cb32ac1eba51'

visitor_indexes = initial_table.index[initial_table['visitorId'] == visitor].tolist()
#initial_table = initial_table[initial_table['visitorId'] != visitor]
#initial_table = initial_table.reset_index(drop=True)

pre_data.preprocessing_DNN(initial_table, "./processed_bloomreach_targeting.json")

X, Y, users_table, categories_table, sortedData = dnn_model.preprocess_data("processed_bloomreach_targeting.json")

list_categories = categories_table.columns.values.tolist()

length_x = len(users_table.columns.values.tolist())
length_y = len(list_categories)

dnn_model.create_model(length_x, length_y)

results, predictions, accuracy = dnn_model.train_model(X, Y)

