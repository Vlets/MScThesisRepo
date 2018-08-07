from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
from MasterProject.NeuralNetwork.NNModel import NNModel
from sklearn.model_selection import train_test_split
from keras.callbacks import EarlyStopping
from sklearn.model_selection import KFold
from random import randint
import pandas as pd
import numpy as np

original_data_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_15mb.json"
no_transactions_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_no_transactions_15mb.json"
normalized_personas_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_everything_15mb.json"
items_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_items_15mb.json"
all_data_processed_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_hellermanntyton_15mb.json"


def calculate_precision(predictions, test_data):
    value_results = pd.DataFrame(0, index=np.arange(len(test_data)), columns=["precision"])
    columns = [x for x in range(len(test_data[0]))]
    length = len(test_data)
    x = 0
    while x < length:
        values1 = predictions[x]
        values2 = test_data[x]
        tp = len([y for y in columns if values1[y] == 1 and values2[y] == 1])
        fn = len([y for y in columns if values1[y] == 0 and values2[y] == 1])
        value_results.loc[x] = tp / (tp + fn)
        x += 1

    precision_values = value_results.precision.values.tolist()

    return sum(precision_values) / len(precision_values)


def random_baseline(testing_x, testing_y):
    training_rows, training_columns = testing_y.shape
    testing_rows, testing_columns = testing_x.shape
    binary_maximum_value = [1] * training_columns
    string_binary_value = ''.join(str(e) for e in binary_maximum_value)
    maximum_value = int(string_binary_value, 2)
    predictions = []
    i = 0

    while i < testing_rows:
        random_value = randint(0, maximum_value)
        string_binary_random_value = "{0:b}".format(random_value)
        list_string_binary_random_value = []
        list_string_binary_random_value[:0] = string_binary_random_value
        list_integer_binary_random_value = [int(x) for x in list_string_binary_random_value]
        size_binary_random_value = len(list_integer_binary_random_value)
        if size_binary_random_value != training_columns:
            difference = training_columns - size_binary_random_value
            zeros = [0] * difference
            zeros.extend(list_integer_binary_random_value)
            list_integer_binary_random_value = zeros

        predictions.append(list_integer_binary_random_value)
        i += 1

    return predictions


def calculate_threshold(model, test_x, test_y):
    predictions = model.predict(test_x)
    predictions_as_table = pd.DataFrame(predictions)
    actual_output = pd.DataFrame(test_y)
    result = []

    for index, row in actual_output.iterrows():
        t = actual_output.loc[index, (actual_output != 0).any(axis=0)]
        p = predictions_as_table.loc[index]
        inter = t[t == 1]
        value_indexes = inter.index.values.tolist()
        prediction_values = p[value_indexes].values.tolist()
        average = sum(prediction_values)/len(prediction_values)
        result.append(average)

    threshold = float("{:1.2f}".format(sum(result)/len(result)))
    return threshold


def run():
    initial_table = pd.read_json(all_data_processed_file_path).reset_index(drop=True)
    items_table = pd.read_json(items_file_path).reset_index(drop=True)
    list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

    nn_model = NNModel()

    data, keywords = nn_model.split_users_data_and_keywords_data(initial_table, list_keywords)

    data_rows, data_columns = data.shape
    keywords_rows, keywords_columns = keywords.shape
    """nn_model.create_model(data_columns, keywords_columns)

train_x, test_x, train_y, test_y = train_test_split(data, keywords, test_size=0.2)
nn_model.train_model(train_x, train_y)

loss, metric = nn_model.model.evaluate(test_x, test_y)
predictions = random_baseline(test_x, test_y)
metric_random = nn_model.calculate_accuracy(predictions, test_y)"""

    kf = KFold(n_splits=7, shuffle=True)
    threshold = []
    scores = []
    for train_index, test_index in kf.split(data):
        print("TRAIN:", train_index, "TEST:", test_index)
        model = nn_model.create_model(data_columns, keywords_columns)
        train_x, test_x = data[train_index], data[test_index]
        train_y, test_y = keywords[train_index], keywords[test_index]
        early_stopping_accuracy = EarlyStopping(monitor='val_acc', min_delta=0.00001, patience=2, verbose=0, mode='auto')
        early_stopping_precision = EarlyStopping(monitor='val_precision', min_delta=0.00001, patience=2, verbose=0, mode='max')
        model.fit(train_x, train_y, epochs=20, batch_size=512, validation_split=0.2,
                  callbacks=[
                      early_stopping_precision,
                      early_stopping_accuracy
                  ])
        loss, metric_precision, metric_accuracy = model.evaluate(test_x, test_y)
        model_threshold = calculate_threshold(model, test_x, test_y)
        random_predictions = random_baseline(test_x, test_y)
        random_precision = calculate_precision(random_predictions, test_y)
        random_accuracy = nn_model.calculate_accuracy(random_predictions, test_y)
        scores.append((metric_precision,
                       metric_accuracy,
                       random_precision,
                       random_accuracy
                       ))
        threshold.append(model_threshold)

    return scores, threshold
