from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from RecommenderSystem.Joana.RecommenderSystemMain import RecommenderSystemMain
import pandas as pd

# Process the data
url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/processed_bloomreach_targeting_20mb.json"


def NN_format_preprocess(data_to_process):
    result_cities = pd.get_dummies(data_to_process['geo_city'])
    result_continent = pd.get_dummies(data_to_process['geo_continent'])
    result_country = pd.get_dummies(data_to_process['geo_country'])
    result_persona_id = pd.get_dummies(data_to_process['personaIdScores_id'])
    result_global_persona_id = pd.get_dummies(data_to_process['globalPersonaIdScores_id'])
    users_table = data_to_process.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id',
                                                'globalPersonaIdScores_id'])
    users_table = pd.concat([users_table,
                             result_cities, result_continent, result_country, result_persona_id,
                             result_global_persona_id], axis=1)

    return users_table

"""

pre_data = PreprocessingData()


pre_data.json_files_preprocess(url, url_no_trans, url_after_everything)

#Process the data to be acceptable by the DNN
pre_data.create_items_table_and_add_paths(url_no_trans, url_after_everything, url_items_file, url_to_save)
"""

main = RecommenderSystemMain()

initial_table = pd.read_json(url_to_save).reset_index(drop=True)
initial_table = NN_format_preprocess(initial_table)
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
    guessed_items, guessed_keywords = main.precision_main(initial_table_to_give, items_table_to_give,
                                                          list_keywords_to_give, visitor, 10)
    precision_items.append(guessed_items)
    precision_keywords.append(guessed_keywords)
    i += 1
    if i % 10 == 0:
        print("Progress Precision:", round((i / visitor_length) * 100, 2), "%")

