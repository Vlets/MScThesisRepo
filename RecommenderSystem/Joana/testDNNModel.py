from RecommenderSystem.NeuralNetwork.DNNModel import DNNModel

dnn_model = DNNModel()

X, Y, X_visitors, Y_visitors, users_table, visitors_table, categories_table, categories_tables_visitors, sortedData = \
    dnn_model.preprocess_data("processed_table_3.json", [])

list_categories = categories_table.columns.values.tolist()

length_x = len(users_table.columns.values.tolist())
length_y = len(list_categories)

dnn_model.create_model(length_x, length_y)

results, predictions, accuracy = dnn_model.train_model(X, Y)