from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from MasterProject.SimilarityAlgorithms.CalculateSimilarity import CalculateSimilarity as cs
from MasterProject.NeuralNetwork.NNModel import NNModel
import pandas as pd
import numpy as np


class RecommenderSystem:
    """
    This is the class where the magic happens.
    For, it is only programmed to run with cold-start scenarios and calculate the precision
    """

    def __init__(self):
        self.predicted_keywords = None

    @staticmethod
    def remove_duplicates(duplicate):
        final_list = []
        for num in duplicate:
            if num not in final_list:
                final_list.append(num)
        return final_list

    def to_filter_items_function(self, list_keywords):
        """
        This method is used to help filter out the unwanted items.
        It checks if the item has at least one of the predicted keywords.
        :param list_keywords: keywords associated to a specific item
        :param self.predicted_keywords: predicted keywords from the NN
        :return: the given keywords if true; else an empty list.
        This will later help in deleting the unwanted items.
        """
        ls1 = sorted([element for element in list_keywords if element in self.predicted_keywords])
        ls2 = sorted([element for element in self.predicted_keywords if element in list_keywords])

        if ls1 == ls2 and ls1 != []:
            return list_keywords

        else:
            return []

    @staticmethod
    def get_seen_items_table_list(table, items_table):
        """
        This method creates a data frame and list of all items in the
        transactionPath column values in the given table.
        :param table: Table with the transaction paths to check the items
        :param items_table: The items table which s used to identify the items in the table
        :return: Data frame and a list of the seen items.
        """
        lst = PreprocessingData.create_list_all_possible_values(table, 'transactionPath')
        lst = [x for x in lst if x in items_table.pageUrl.unique().tolist()]
        table_result = items_table.loc[items_table['pageUrl'].isin(lst)][['pageUrl', 'keywords']]

        return table_result, lst

    @staticmethod
    def prepare_data_to_calculate_similarity(items_with_predicted_keywords, user_seen_items_table):
        """
        This method prepares the items with predicted keywords data and items
        previously seen by the user data to be later used when calculating
        similarities between them
        :param items_with_predicted_keywords: Data frame with the items not
        seen by the user
        :param user_seen_items_table: Data frame with the items seen previously
        bythe user
        :return: List of tuples with URLs of unseen items and their associated
        keywords and a list of lists of keywords of each seen item
        """

        # Turn keywords into strings
        items_with_predicted_keywords['keywords'] = items_with_predicted_keywords.keywords.apply(
            " ".join)
        user_seen_items_table['keywords'] = user_seen_items_table.keywords.apply(" ".join)

        # Get list of keywords of each item
        seen_items_keywords = user_seen_items_table.keywords.values.tolist()
        filtered_items_keywords = items_with_predicted_keywords.keywords.values.tolist()

        # Get list of pageUrls
        filtered_items_urls = items_with_predicted_keywords.pageUrl.values.tolist()

        # Zip the keywords and pageUrls
        filtered_items_tuples = list(zip(filtered_items_urls, filtered_items_keywords))

        return filtered_items_tuples, seen_items_keywords

    def get_seen_unseen_items(self, initial_table, items_table, user_id):
        """
        This method creates two data frames, one with seen items by the user
        with id user_id and their respective keywords, one with unseen
        items by the user and their respective keywords
        :param initial_table: The whole dataset
        :param items_table: The items table
        :param user_id: The id of the user
        :return: Data frame with seen item by the user with their respective
        keywords; Data frame with items not seen by the user
        """

        # Get table with items that have the keywords found previously
        items_with_predicted_keywords = items_table.copy()
        items_with_predicted_keywords['keywords'] = items_with_predicted_keywords.keywords.apply(
            self.to_filter_items_function)
        items_with_predicted_keywords = items_with_predicted_keywords[
            items_with_predicted_keywords.astype(str)['keywords'] != '[]'].reset_index(drop=True)

        # Get visitor past viewed items from the initial_table
        user_previous_paths = initial_table.loc[initial_table['visitorId'] == user_id]
        user_seen_items_table, user_seen_items_list = RecommenderSystem.get_seen_items_table_list(
            user_previous_paths, items_table)

        # Remove the seen items in filtered items
        items_with_predicted_keywords = items_with_predicted_keywords[
            (~items_with_predicted_keywords.pageUrl.isin(user_seen_items_table))]

        return items_with_predicted_keywords, user_seen_items_table

    def turn_predicted_keywords_to_string_values(self, list_keywords, user_keywords_predictions):
        """
        This method gets the string values of the predicted keywords
        :param list_keywords: Lis of all possible values of keywords
        :param user_keywords_predictions: Vector with the predicted
        keywords
        :return: Nothing, it saves on the global variable the string values
        of the predicted keywords
        """

        # Turn the predictions into table
        predictions_as_table = pd.DataFrame(user_keywords_predictions)

        # Delete the columns with only 0 as their values
        predictions_as_table = predictions_as_table.loc[:, (predictions_as_table != 0).any(axis=0)]

        # Get the indexes of the predicted keywords in list_keywords
        predicted_keywords_indexes = predictions_as_table.columns.values.tolist()

        # Get the actual keywords
        predicted_keywords = [list_keywords[x] for x in predicted_keywords_indexes]

        #FOR TESTING PURPOSES ONLY
        # predicted_keywords = [x for x in predicted_keywords if x not in for_test]

        self.predicted_keywords = predicted_keywords

    @staticmethod
    def create_and_train_nn(nn_model, training_data, training_keywords):
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

    @staticmethod
    def calculate_similarities(filtered_items_tuples, seen_items_keywords):
        """
        This method makes the calculation of similarities
        :param filtered_items_tuples: List od tuples with the URLs and
        keywords of unseen items
        :param seen_items_keywords: List of lists of keywords associated
        to each seen item
        :return: A list of suggested items
        """

        final_result = sorted(cs.similarity_results(seen_items_keywords, filtered_items_tuples))[::-1]
        final_result_items = [y for x, y in final_result]
        final_result_items = RecommenderSystem.remove_duplicates(final_result_items)

        return final_result_items

    def suggest_items(self, initial_table, items_table, list_keywords, prediction_testing_data, user_id):

        # Get the predicted keywords
        self.turn_predicted_keywords_to_string_values(list_keywords, prediction_testing_data)

        # Get the table with seen items from user past visits and table with unseen items
        items_with_predicted_keywords, user_seen_items_table = self.get_seen_unseen_items(initial_table, items_table,
                                                                                          user_id)

        # Prepare the data to then calculate similarities
        filtered_items_tuples, seen_items_keywords = self.prepare_data_to_calculate_similarity(
            items_with_predicted_keywords, user_seen_items_table)

        # Calculate similarities based on their keywords
        final_result_items = self.calculate_similarities(filtered_items_tuples, seen_items_keywords)

        return final_result_items

    def run_recommender_system(self, initial_table, items_table, list_keywords, user_data, user_id):
        """
        This method runs the whole project. This is how the recommender systems would work.
        :param user_id:
        :param user_data: The data of the user to be used in the process
        :param initial_table: The database in its original state (after processing)
        :param items_table: The table with the urls of items and their associated keywords
        :param list_keywords: A list of all possible values of keywords based on the items_table
        :return: The precision of the systems
        """
        nn_model = NNModel()

        # Data used to train the DNN.
        training_data, training_keywords = nn_model.split_users_data_and_keywords_data(initial_table, list_keywords)
        testing_data = user_data.iloc[:, :].values

        # Create and train the NN model
        self.create_and_train_nn(nn_model, training_data, training_keywords)

        # The chosen input data to give to NN to predict
        testing_data = np.array([testing_data[0].tolist()])

        # The predictions from the NN based on the given input
        prediction_testing_data = nn_model.predict_values(testing_data)

        final_result_items = self.suggest_items(initial_table, items_table, list_keywords, prediction_testing_data,
                                                user_id)

        return final_result_items


