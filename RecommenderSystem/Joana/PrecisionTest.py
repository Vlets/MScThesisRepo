from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from RecommenderSystem.Joana.Main import Main
import pandas as pd

# Process the data
url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_20mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_no_transactions_20mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_everything_20mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_items_20mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/processed_bloomreach_targeting_20mb.json"


"""
pre_data = PreprocessingData()


pre_data.run_preprocessing(url, url_no_trans, url_after_everything)

#Process the data to be acceptable by the DNN
pre_data.preprocessing_DNN(url_no_trans, url_after_everything, url_items_file, url_to_save)
"""

main = Main()

initial_table = pd.read_json(url_to_save).reset_index(drop=True)
items_table = pd.read_json(url_items_file).reset_index(drop=True)

list_categories = PreprocessingData.create_list(items_table, 'categories_terms')

groups = initial_table.groupby('visitorId').count()

returning_visitors = groups.index[groups['transactionPath'] > 1].tolist()

precision = []

i = 0
visitor_length = len(returning_visitors)

for visitor in returning_visitors:
    initial_table_to_give = initial_table.copy()
    items_table_to_give = items_table.copy()
    list_categories_to_give = list_categories.copy()
    precision.append(main.run_main(initial_table_to_give, items_table_to_give, list_categories_to_give, visitor, 10))
    i += 1
    if i % 100 == 0:
        print("Progress Precision:", round((i / visitor_length) * 100, 2), "%")