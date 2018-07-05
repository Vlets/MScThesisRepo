from RecommenderSystem.NeuralNetwork.DNNModel import DNNModel
import pandas as pd

dnn_model = DNNModel()

table = pd.read_json('/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/Joana/processed_table_3.json').reset_index(drop=True)