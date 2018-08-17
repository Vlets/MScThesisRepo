from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.Evaluation.Evaluation import prepare_training_testing_data
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
import pandas as pd
import numpy as np

original_data_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_15mb.json"
no_transactions_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_no_transactions_15mb.json"
normalized_personas_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_everything_15mb.json"
items_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_items_15mb.json"
all_data_processed_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_hellermanntyton_15mb.json"


def make_count_table(user_seen_items, user_seen_keywords, items_table):
    count_table = pd.DataFrame(0, index=np.arange(1), columns=user_seen_keywords)
    seen_items = items_table[items_table['pageUrl'].isin(user_seen_items)]

    for index, row in seen_items.iterrows():
        values = row['keywords']
        values = [x for x in values if x in user_seen_keywords]
        count_table.loc[0, values] += 1

    return count_table


def run_pipeline():
    # 1st, pre-process the whole data
    pre_data = PreprocessingData()
    pre_data.data_pre_process(original_data_path, no_transactions_file_path, normalized_personas_file_path,
                              items_file_path, all_data_processed_file_path)

    # 2nd, initialize the recommender system
    main = RecommenderSystem()

    # 3rd, gather all the processed data
    initial_table = pd.read_json(all_data_processed_file_path).reset_index(drop=True)
    items_table = pd.read_json(items_file_path).reset_index(drop=True)
    list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

    # 4th, prepare the training and testing data
    # user_id = '2da0f833-c9a8-41fa-86d5-bb179633b87a'
    user_id = 'e38507e2-fcb3-448c-a52b-02ce50056d58'

    actual_seen_items_list, training_data, user_actual_seen_keywords, testing_data, user_actual_output, user_past_visits \
        = prepare_training_testing_data(initial_table, items_table, list_keywords, user_id)

    # count_table = make_count_table(actual_seen_items_list, user_actual_seen_keywords, items_table)
    # irrelevant_keywords = count_table.loc[:, (count_table <= 15).any(axis=0)].columns.values.tolist()

    # 5th, run the recommender system
    suggested_items = main.run_recommender_system(training_data, items_table, list_keywords, testing_data, user_id)

    correctly_predicted_items = [x for x in suggested_items if x in actual_seen_items_list]
    indexes_of_correctly_guessed_items = [suggested_items.index(value) for value in correctly_predicted_items]
    predicted_correctly_keywords = [x for x in main.predicted_keywords if x in user_actual_seen_keywords]

    return suggested_items, correctly_predicted_items, indexes_of_correctly_guessed_items, predicted_correctly_keywords, \
           main.predicted_keywords


returned_items, correctly_guessed_items, indexes_of_correctly_guessed_items, correctly_guessed_keywords, \
   predicted_keywords = run_pipeline()
