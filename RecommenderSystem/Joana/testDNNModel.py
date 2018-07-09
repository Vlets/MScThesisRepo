from RecommenderSystem.NeuralNetwork.NNModel import NNModel
import pandas as pd

dnn_model = NNModel()

table = pd.read_json('/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/Joana/processed_table_3.json').reset_index(drop=True)