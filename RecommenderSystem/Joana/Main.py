from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from RecommenderSystem.DataAlgorithms.CalculateSimilarity import CalculateSimilarity as cs
from RecommenderSystem.NeuralNetwork.DNNModel import DNNModel
import pandas as pd
import numpy as np


class Main:
    """
    This is the class where the magic happens.
    For, it is only programmed to run with cold-start scenarios and calculate the precision
    """

    def __init__(self):
        self.predicted_keywords = None

    def to_filter_function(self, lst1):
        """
        This method is used to help filter out the unwanted items.
        It checks if the item has at least one of the predicted keywords.
        :param lst1: keywords associated to a specific item
        :param self.predicted_keywords: predicted keywords from the NN
        :return: the given keywords if true; else an empty list.
        This will later help in deleting the unwanted items.
        """
        ls1 = [element for element in lst1 if element in self.predicted_keywords]
        ls2 = [element for element in self.predicted_keywords if element in lst1]

        if ls1 == ls2 and ls1 != []:
            return lst1

        else:
            return []

    @staticmethod
    def get_seen_items_table_list(table, it_table):
        """
        This method creates a data frame and list of all items in the
        transactionPath column values in the given table.
        :param table: Table with the transaction paths to check the items
        :param it_table: The items table which s used to identify the items in the table
        :return: Data frame and a list of the seen items.
        """
        lst = PreprocessingData.create_list(table, 'transactionPath')
        lst = [x for x in lst if x in it_table.pageUrl.unique().tolist()]
        table_result = it_table.loc[it_table['pageUrl'].isin(lst)][['pageUrl', 'categories_terms']]

        return table_result, lst

    @staticmethod
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
        actual_seen_items_table, actual_seen_items_list = Main.get_seen_items_table_list(user_visits, items_table)
        user_actual_seen_keywords = PreprocessingData.create_list(user_visits, 'categories')

        # Drop the unwanted visits from initial_table
        initial_table = initial_table.drop(user_indexes).reset_index(drop=True)

        user_visits = user_visits.drop(columns=list_keywords).reset_index(drop=True)

        main = Main()

        final_result_items = main.run_main(initial_table, items_table, list_keywords, user_visits)

        correctly_predicted_items = [x for x in final_result_items if x in actual_seen_items_list]
        indexes = [final_result_items.index(value) for value in correctly_predicted_items]

        count_correct_guessed_items = len([x for x in indexes if x < k])
        count_correct_guessed_keywords = len([x for x in main.predicted_keywords if x in user_actual_seen_keywords])

        return count_correct_guessed_items / k, count_correct_guessed_keywords / len(main.predicted_keywords)

    def run_main(self, initial_table, items_table, list_keywords, user_data):
        """
        This method runs the whole project. This is how the recommender systems would work.
        :param user_data: The data of the user to be used in the process
        :param initial_table: The database in its original state (after processing)
        :param items_table: The table with the urls of items and their associated keywords
        :param list_keywords: A list of all possible values of keywords based on the items_table
        :return: The precision of the systems
        """
        dnn_model = DNNModel()

        user_id = user_data.loc[0, 'visitorId']

        # - Data used to train the DNN.
        # - Users_data is the input data to give to NN to train based on the initial_table
        # - Users_keywords is the output data to give to NN to train based on the initial_table
        # - User_data_to_test is the input data to give to NN to predict the output based on user_visits
        # - Users_table is the input data in a format of data frame
        # - Keywords_table is the output data in a format of data frame
        users_data, users_keywords, user_data_to_test, users_table, keywords_table = \
            dnn_model.preprocess_data(initial_table, user_data, list_keywords)

        # Dimension of the input data
        length_x = len(users_table.columns.values.tolist())

        # Dimension of the output data
        length_y = len(keywords_table.columns.values.tolist())

        # Create Neural Network model with the calculated dimensions
        dnn_model.create_model(length_x, length_y)

        # Training the NN
        dnn_model.train_model(users_data, users_keywords)

        # The chosen input data to give to NN to predict
        user_data_to_give = np.array([user_data_to_test[0].tolist()])
        # user_keywords_to_predict = np.array([hidden_user_keywords[0].tolist()])

        # The predictions from the NN based on the given input
        user_keywords_predictions = dnn_model.predict_values(user_data_to_give)
        # visitors_accuracy = DNNModel.calculate_accuracy(visitors_prediction, test_value_y)

        # Turn the predictions into table
        predictions_as_table = pd.DataFrame(user_keywords_predictions)

        # Delete the columns with only 0 as their values
        predictions_as_table = predictions_as_table.loc[:, (predictions_as_table != 0).any(axis=0)]

        # Get the indexes of the predicted keywords in list_keywords
        predicted_keywords_indexes = predictions_as_table.columns.values.tolist()

        # Get the actual keywords
        predicted_keywords = [list_keywords[x] for x in predicted_keywords_indexes]
        self.predicted_keywords = predicted_keywords

        # Get table with items that have the keywords found previously
        items_with_predicted_keywords = items_table.copy()
        items_with_predicted_keywords['categories_terms'] = items_with_predicted_keywords.categories_terms.apply(
            self.to_filter_function)
        items_with_predicted_keywords = items_with_predicted_keywords[
            items_with_predicted_keywords.astype(str)['categories_terms'] != '[]'].reset_index(drop=True)

        # Get visitor past viewed items from the initial_table
        user_previous_paths = initial_table.loc[initial_table['visitorId'] == user_id]
        user_seen_items_table, user_seen_items_list = Main.get_seen_items_table_list(user_previous_paths, items_table)
        user_seen_items_table = user_seen_items_table.reset_index(drop=True)

        # Remove the seen items in filtered items
        items_with_predicted_keywords = items_with_predicted_keywords[
            (~items_with_predicted_keywords.pageUrl.isin(user_seen_items_table))]

        # Turn keywords into strings
        items_with_predicted_keywords['categories_terms'] = items_with_predicted_keywords.categories_terms.apply(
            " ".join)
        user_seen_items_table['categories_terms'] = user_seen_items_table.categories_terms.apply(" ".join)

        # Get list of keywords of each item
        seen_items_keywords = user_seen_items_table.categories_terms.values.tolist()
        filtered_items_keywords = items_with_predicted_keywords.categories_terms.values.tolist()

        # Get list of pageUrls
        #seen_items_urls = user_seen_items_table.pageUrl.values.tolist()
        filtered_items_urls = items_with_predicted_keywords.pageUrl.values.tolist()

        # Zip the ckeywords and pageUrls
        #seen_items_tuples = list(zip(seen_items_urls, seen_items_keywords))
        filtered_items_tuples = list(zip(filtered_items_urls, filtered_items_keywords))

        # Calculate similarities based on their keywords
        final_result = sorted(cs.similarity_results(seen_items_keywords, filtered_items_tuples))[::-1]
        final_result_items = [y for x, y in final_result]
        final_result_items = PreprocessingData.remove_duplicates(final_result_items)

        return final_result_items
