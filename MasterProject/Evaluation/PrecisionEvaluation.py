from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.RecommenderSystem.RecommenderSystem import RecommenderSystem
import pandas as pd

# Process the data
url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/MasterProject/FilesToTest/processed_bloomreach_targeting_20mb.json"


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
    user_indexes = user_visits.index.values.tolist()

    # Choose visit to keep in initial_table
    index_to_drop = user_indexes[0]

    # Drop the visit to keep in initial_table from user_visits table
    user_visits = user_visits.drop(index_to_drop)

    # Remove the index of visit to keep from list of indexes of user in initial_table
    user_indexes.remove(index_to_drop)

    # From the user_visits table, get the items he has seen
    actual_seen_items_table, actual_seen_items_list = RecommenderSystem.get_seen_items_table_list(user_visits,
                                                                                                  items_table)
    user_actual_seen_keywords = PreprocessingData.create_list_all_possible_values(user_visits, 'keywords')

    # Drop the unwanted visits from initial_table
    initial_table = initial_table.drop(user_indexes).reset_index(drop=True)

    user_visits = user_visits.drop(columns=list_keywords)
    user_visits = user_visits.drop(columns=['keywords', 'transactionPath', 'visitorId'])

    return actual_seen_items_list, initial_table, user_actual_seen_keywords, user_visits


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
    actual_seen_items_list, initial_table, user_actual_seen_keywords, user_visits = \
        prepare_training_testing_data(initial_table, items_table, list_keywords, user_id)

    main = RecommenderSystem()

    final_result_items = main.run_main(initial_table, items_table, list_keywords, user_visits, user_id)

    correctly_predicted_items = [x for x in final_result_items if x in actual_seen_items_list]
    indexes = [final_result_items.index(value) for value in correctly_predicted_items]

    count_correct_guessed_items = len([x for x in indexes if x < k])
    count_correct_guessed_keywords = len([x for x in main.predicted_keywords if x in user_actual_seen_keywords])

    return count_correct_guessed_items / k, count_correct_guessed_keywords / len(main.predicted_keywords)


def run_evaluation():
    initial_table = pd.read_json(url_to_save).reset_index(drop=True)
    items_table = pd.read_json(url_items_file).reset_index(drop=True)

    list_keywords = PreprocessingData.create_list_all_possible_values(items_table, 'keywords')

    groups = initial_table.groupby('visitorId').count()

    returning_visitors = groups.index[groups['transactionPath'] > 1].tolist()

    precision_items = []
    precision_keywords = []

    i = 0
    visitor_length = len(returning_visitors)

    for visitor in returning_visitors:
        initial_table_to_give = initial_table.copy()
        items_table_to_give = items_table.copy()
        list_keywords_to_give = list_keywords.copy()
        guessed_items, guessed_keywords = precision_main(initial_table_to_give, items_table_to_give,
                                                         list_keywords_to_give, visitor, 5)
        precision_items.append(guessed_items)
        precision_keywords.append(guessed_keywords)
        i += 1
        if i % 10 == 0:
            print("Progress Precision:", round((i / visitor_length) * 100, 2), "%")

    return precision_items, precision_keywords

precision_items, precision_keywords = run_evaluation()