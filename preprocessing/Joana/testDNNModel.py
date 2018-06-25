from preprocessing.Joana.DNNModel import DNNModel

dnn_model = DNNModel()

X, Y, users_table, categories_table, sortedData = dnn_model.preprocess_data("processed_table_3.json")

list_categories = categories_table.columns.values.tolist()

length_x = len(users_table.columns.values.tolist())
length_y = len(list_categories)

dnn_model.create_model(length_x, length_y)

results, predictions, accuracy = dnn_model.train_model(X, Y)