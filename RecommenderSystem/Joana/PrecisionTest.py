from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
import pandas as pd

url = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_50mb.json"
url_no_trans = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_no_transactions_50mb.json"
url_after_everything = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_everything_50mb.json"
url_items_file = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_items_50mb.json"
url_to_save = "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/processed_bloomreach_targeting_50mb.json"

initial_table = pd.read_json(url_to_save).reset_index(drop=True)
items_table = pd.read_json(url_items_file).reset_index(drop=True)

list_categories = PreprocessingData.create_list(items_table, 'categories_terms')

groups = initial_table.goruby('visitorId').count()

returning_visitors = groups.index[groups['transactionPath'] > 1]

for visitor in returning_visitors:
    visitor_table = initial_table[initial_table['visitorId'] == visitor]