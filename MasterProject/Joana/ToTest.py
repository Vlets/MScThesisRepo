from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
from MasterProject.NeuralNetwork.NNModel import NNModel
import pandas as pd
import numpy as np

url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_bloomreach_targeting_20mb.json"


def create_and_train_NN(nn_model, training_data, training_keywords):
    """
    This method creates and trains a Neural Network model with the
    given data
    :param nn_model: Class used to create and train the Neural Network
    :param training_data: Data used for training as input data
    :param training_keywords: Data used for training as output data
    :return: Nothing
    """

    data_rows, data_columns = training_data.shape

    keywords_rows, keywords_columns = training_keywords.shape

    nn_model.create_model(data_columns, keywords_columns)

    nn_model.train_model(training_data, training_keywords)


main = RecommenderSystem()

initial_table = pd.read_json(url_to_save).reset_index(drop=True)
items_table = pd.read_json(url_items_file).reset_index(drop=True)

list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')
user_id = '2da0f833-c9a8-41fa-86d5-bb179633b87a'

# Get previous visits from user with user_id into a table
user_visits = initial_table[initial_table['visitorId'] == user_id]

# Get the indexes of the user from the initial_table
user_indexes = user_visits.index.values.tolist()

# Choose visit to keep in initial_table
index_to_drop = user_indexes[0]

# Drop the visit to keep in initial_table from user_visits table
user_visits = user_visits.drop(index_to_drop)

# Remove the index of visit to keep from lis of indexes of user in initial_table
user_indexes.remove(index_to_drop)

# From the user_visits table, get the items he has seen
actual_seen_items_table, actual_seen_items_list = RecommenderSystem.get_seen_items_table_list(user_visits,
                                                                                              items_table)
user_actual_seen_keywords = PreprocessingData.create_list_all_possible_values(user_visits, 'keywords')

# Drop the unwanted visits from initial_table
initial_table = initial_table.drop(user_indexes).reset_index(drop=True)

user_visits_keywords = user_visits[list_keywords]

user_visits = user_visits.drop(columns=list_keywords)
user_visits = user_visits.drop(columns=['keywords', 'transactionPath', 'visitorId'])


nn_model = NNModel()

# Data used to train the DNN.
training_data, training_keywords = nn_model.split_users_data_and_keywords_data(initial_table, list_keywords)
testing_data = user_visits.iloc[:, :].values

create_and_train_NN(nn_model, training_data, training_keywords)
# testing_data = np.array([testing_data[0].tolist()])

# The predictions from the NN based on the given input
prediction_testing_data = nn_model.predict_values(testing_data)
# Turn the predictions into table
predictions_as_table = pd.DataFrame(prediction_testing_data)

# Delete the columns with only 0 as their values
# predictions_as_table = predictions_as_table.loc[:, (predictions_as_table >= 0.5).any(axis=0)]

