from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
from MasterProject.NeuralNetwork.NNModel import NNModel
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

original_data_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_20mb.json"
no_transactions_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
normalized_personas_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_everything_20mb.json"
items_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_items_20mb.json"
all_data_processed_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_bloomreach_targeting_20mb.json"

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

    nn_model.train_model(training_data, training_keywords, graphs=True)


main = RecommenderSystem()

initial_table = pd.read_json(all_data_processed_file_path).reset_index(drop=True)
items_table = pd.read_json(items_file_path).reset_index(drop=True)
list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

user_id = '2da0f833-c9a8-41fa-86d5-bb179633b87a'
# user_id = 'e38507e2-fcb3-448c-a52b-02ce50056d58'

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

"""
def threshold():
    initial_table = pd.read_json(url_to_save).reset_index(drop=True)
    items_table = pd.read_json(url_items_file).reset_index(drop=True)

    list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

    groups = initial_table.groupby('visitorId').count()

    returning_visitors = groups.index.tolist()

    guess = []

    for visitor in returning_visitors:
        visits = initial_table[initial_table['visitorId'] == visitor]
        indexes = user_visits.index.values.tolist()
        to_drop_index = user_indexes[0]
        t = user_visits_keywords.loc[1254, (user_visits_keywords != 0).any(axis=0)]
        p = predictions_as_table.loc[1]
        res = t[t == 1]
        words = res.index.values.tolist()
        ind = [list_keywords.index(x) for x in words]
        result = p[ind]
        values = result.values.tolist()
        sum(values) / len(values)
"""