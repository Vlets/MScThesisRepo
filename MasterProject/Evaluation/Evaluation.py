from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
import random
import pandas as pd
import numpy as np

# Process the data
original_data_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_15mb.json"
no_transactions_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_no_transactions_15mb.json"
normalized_personas_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_everything_15mb.json"
items_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/hellermanntyton_items_15mb.json"
all_data_processed_file_path = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_hellermanntyton_15mb.json"


def calculate_accuracy(list_keywords, true_values, predicted_values):
    tp = len([x for x in list_keywords if x in predicted_values and x in true_values])
    tn = len([x for x in list_keywords if x not in predicted_values and x not in true_values])
    fp = len([x for x in list_keywords if x in predicted_values and x not in true_values])
    fn = len([x for x in list_keywords if x not in predicted_values and x in true_values])

    accuracy = (tp + tn) / (tp + tn + fp + fn)

    return accuracy


def random_items_prediction_precision(items_table, user_past_visits, actual_seen_items_list, k):
    list_of_items = items_table.pageUrl.values.tolist()
    items_already_seen_table, items_already_seen_list = RecommenderSystem.get_seen_items_table_list(user_past_visits,
                                                                                                    items_table)
    list_of_items_to_suggest = [x for x in list_of_items if x not in items_already_seen_list]
    random.shuffle(list_of_items_to_suggest)

    random_correctly_predicted_items = [x for x in list_of_items_to_suggest if x in actual_seen_items_list]
    indexes_random = [list_of_items_to_suggest.index(value) for value in random_correctly_predicted_items]

    count_correct_random_guessed_items = len([x for x in indexes_random if x < k])

    return count_correct_random_guessed_items / k


def make_count_table(user_seen_items, user_seen_keywords, items_table):
    count_table = pd.DataFrame(0, index=np.arange(1), columns=user_seen_keywords)
    seen_items = items_table[items_table['pageUrl'].isin(user_seen_items)]

    for index, row in seen_items.iterrows():
        values = row['keywords']
        values = [x for x in values if x in user_seen_keywords]
        count_table.loc[0, values] += 1

    return count_table


def prepare_training_testing_data(initial_table, items_table, list_keywords, user_id):
    """
    This method prepares the data to be used when evaluating the precision
    of the system in cold-start scenarios
    :param initial_table: The whole data set
    :param items_table: The items table
    :param list_keywords: List of all possible keywords based on the items
    table
    :param user_id: The id of user to be used when evaluating the precision
    in cold-start scenarios
    :return: A list of items seen bu the user with id user_id; The whole
    data set with changes; The keywords from the items actually seen
    by the user; The data about the user; The id of user
    """

    # Get previous visits from user with user_id into a table
    user_visits = initial_table[initial_table['visitorId'] == user_id]

    # Get the indexes of the user from the initial_table
    user_indexes_in_initial_table = user_visits.index.values.tolist()

    # Choose visit to keep in initial_table
    index_to_keep_in_initial_table = user_indexes_in_initial_table[0]

    # Drop the visit to keep in initial_table from user_visits table
    user_past_visits = user_visits[user_visits.index == index_to_keep_in_initial_table]
    user_visits = user_visits.drop(index_to_keep_in_initial_table)

    # Remove the index of visit to keep from list of indexes of user in initial_table
    user_indexes_in_initial_table.remove(index_to_keep_in_initial_table)

    # From the user_visits table, get the items he has seen
    actual_seen_items_table, actual_seen_items_list = RecommenderSystem.get_seen_items_table_list(user_visits,
                                                                                                  items_table)
    user_actual_seen_keywords = PreprocessingData.create_list_all_possible_values(user_visits, 'keywords')
    user_actual_output = user_visits[list_keywords]

    # Drop the unwanted visits from initial_table
    initial_table = initial_table.drop(user_indexes_in_initial_table).reset_index(drop=True)

    user_visits = user_visits.drop(columns=list_keywords)
    user_visits = user_visits.drop(columns=['keywords', 'transactionPath', 'visitorId'])

    return actual_seen_items_list, initial_table, user_actual_seen_keywords, user_visits, user_actual_output, \
           user_past_visits


def random_baseline(testing_x, testing_y):
    output_number_rows, output_number_columns = testing_y.shape
    input_number_rows, input_number_columns = testing_x.shape
    only_zeros = [0] * output_number_columns
    top_k = 150
    predictions = []
    i = 0

    while i < input_number_rows:
        list_of_indexes = [x for x in range(0, output_number_columns)]
        random.shuffle(list_of_indexes)
        indexes_to_change = list_of_indexes[:top_k]
        for index in indexes_to_change:
            only_zeros[index] = 1

        predictions.append(only_zeros)
        i += 1

    return predictions


def precision_main(initial_table, items_table, list_keywords, user_id, k):
    """
    This method runs the precision evaluation. Both for predicting the actual items
    and the actual keywords.
    :param initial_table: The whole data base used for the evaluation
    :param items_table: The items found in the whole data base
    :param list_keywords: The all possible keywords from the items table
    :param user_id: The id of user to test
    :param k: Top k items to check the precision
    :return: The precision of predicting the items and precision of predicting the keywords
    """
    actual_seen_items_list, initial_table, user_actual_seen_keywords, user_visits, user_actual_output, user_past_visits \
        = prepare_training_testing_data(initial_table, items_table, list_keywords, user_id)

    # count_table = make_count_table(actual_seen_items_list, user_actual_seen_keywords, items_table)
    # irrelevant_keywords = count_table.loc[:, (count_table == 1).any(axis=0)].columns.values.tolist()

    main = RecommenderSystem()

    final_result_items = main.run_recommender_system(initial_table, items_table, list_keywords, user_visits, user_id)

    correctly_predicted_items = [x for x in final_result_items if x in actual_seen_items_list]
    indexes = [final_result_items.index(value) for value in correctly_predicted_items]

    count_correct_guessed_items = len([x for x in indexes if x < k])
    count_correct_guessed_keywords = len([x for x in main.predicted_keywords if x in user_actual_seen_keywords])

    accuracy = calculate_accuracy(list_keywords, user_actual_seen_keywords, main.predicted_keywords)

    ####################################################################################################################
    # Predict items with randomly predicted keywords
    testing_data = user_visits.iloc[:, :].values
    testing_keywords = user_actual_output.iloc[:, :].values
    test_x = np.array([testing_data[0].tolist()])
    test_y = np.array([testing_keywords[0].tolist()])

    random_keywords_prediction = random_baseline(test_x, test_y)
    random_items_prediction = main.suggest_items(initial_table, items_table, list_keywords, random_keywords_prediction,
                                                 user_id)
    random_correctly_predicted_items = [x for x in random_items_prediction if x in actual_seen_items_list]
    indexes_random = [random_items_prediction.index(value) for value in random_correctly_predicted_items]

    count_correct_random_guessed_items = len([x for x in indexes_random if x < k])
    count_correct_random_guessed_keywords = len([x for x in random_keywords_prediction if x in user_actual_seen_keywords])

    accuracy_keywords_random = calculate_accuracy(list_keywords, user_actual_seen_keywords, random_keywords_prediction)

    ####################################################################################################################
    # Predict items randomly
    items_prediction_random = random_items_prediction_precision(items_table, user_past_visits, actual_seen_items_list,
                                                                k)

    return count_correct_guessed_items / k, count_correct_guessed_keywords / len(main.predicted_keywords), \
           len(correctly_predicted_items) / len(final_result_items), accuracy, count_correct_random_guessed_items / k, \
           items_prediction_random, accuracy_keywords_random, \
           count_correct_random_guessed_keywords / len(random_keywords_prediction)


def run_evaluation():
    initial_table = pd.read_json(all_data_processed_file_path).reset_index(drop=True)
    items_table = pd.read_json(items_file_path).reset_index(drop=True)
    list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

    groups = initial_table.groupby('visitorId').count()

    returning_visitors = groups.index[groups['transactionPath'] > 1].tolist()

    precision_items = []
    precision_keywords = []
    precision_items_overall = []
    accuracy_overall = []
    random_baseline_precision_keywords_items = []
    random_baseline_precision_items = []
    random_baseline_keywords_precision = []
    random_baseline_keywords_accuracy = []

    i = 0
    visitor_length = len(returning_visitors)

    print("Top 3")

    for visitor in returning_visitors:
        initial_table_to_give = initial_table.copy()
        items_table_to_give = items_table.copy()
        list_keywords_to_give = list_keywords.copy()
        guessed_items, guessed_keywords, overall_precision, average_accuracy, random_keywords_items_prediction, \
        random_items_prediction, random_keywords_accuracy, random_keywords_precision \
            = precision_main(initial_table_to_give, items_table_to_give, list_keywords_to_give, visitor, 3)

        precision_items.append(guessed_items)
        precision_keywords.append(guessed_keywords)
        precision_items_overall.append(overall_precision)
        accuracy_overall.append(average_accuracy)
        random_baseline_precision_keywords_items.append(random_keywords_items_prediction)
        random_baseline_precision_items.append(random_items_prediction)
        random_baseline_keywords_precision.append(random_keywords_precision)
        random_baseline_keywords_accuracy.append(random_keywords_accuracy)
        i += 1
        if i % 10 == 0:
            print("Progress Precision:", round((i / visitor_length) * 100, 2), "%")

    return precision_items, precision_keywords, precision_items_overall, accuracy_overall, \
           random_baseline_precision_keywords_items, random_baseline_precision_items, \
           random_baseline_keywords_precision, random_baseline_keywords_accuracy


# precision_items, precision_keywords, precision_items_overall, accuracy_overall, random_keywords_items, random_items, \
# random_keywords_precision, random_keywords_accuracy = run_evaluation()
