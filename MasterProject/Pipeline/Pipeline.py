from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.Evaluation.PrecisionEvaluation import prepare_training_testing_data
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
import pandas as pd

url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_bloomreach_targeting_20mb.json"


def data_pre_process():
    pre_data = PreprocessingData()

    pre_data.json_files_pre_process(url, url_no_trans, url_after_everything)

    # Process the data to be acceptable by the DNN
    pre_data.create_items_table_and_one_hot_encoding(url_no_trans, url_after_everything, url_items_file, url_to_save)


"""def prepare_training_testing_data(initial_table, list_keywords, user_id):
    # Get previous visits from user with user_id into a table
    user_visits = initial_table[initial_table['visitorId'] == user_id]

    # Get the indexes of the user from the initial_table
    user_indexes = user_visits.index.values.tolist()

    # Choose visit to keep in initial_table
    index_to_drop = user_indexes[0]

    # Drop the visit to keep in initial_table from user_visits table
    user_visits = user_visits.drop(index_to_drop)

    # Remove the index of visit to keep from list of indexes of user in initial_table
    user_indexes.remove(index_to_drop)

    # Drop the unwanted visits from initial_table
    initial_table = initial_table.drop(user_indexes).reset_index(drop=True)

    user_visits = user_visits.drop(columns=list_keywords)
    user_visits = user_visits.drop(columns=['keywords', 'transactionPath', 'visitorId'])

    return initial_table, user_visits
"""


def run_pipeline():
    # 1st, pre-process the whole data
    # data_pre_process()

    # 2nd, initialize the recommender system
    main = RecommenderSystem()

    # 3rd, gather all the processed data
    initial_table = pd.read_json(url_to_save).reset_index(drop=True)

    items_table = pd.read_json(url_items_file).reset_index(drop=True)

    list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

    # 4th, prepare the training and testing data
    user_id = '2da0f833-c9a8-41fa-86d5-bb179633b87a'

    actual_seen_items_list, training_data, user_actual_seen_keywords, testing_data = \
        prepare_training_testing_data(initial_table, items_table, list_keywords, user_id)

    # 5th, run the recommender system
    suggested_items = main.run_main(training_data, items_table, list_keywords, testing_data, user_id)

    correctly_predicted_items = [x for x in suggested_items if x in actual_seen_items_list]
    indexes = [suggested_items.index(value) for value in correctly_predicted_items]

    return suggested_items, correctly_predicted_items, indexes


suggested_items, correctly_guessed_items, indexes_of_correctly_guessed_items = run_pipeline()
