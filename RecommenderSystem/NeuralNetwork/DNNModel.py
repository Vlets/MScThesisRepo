from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Importing the Keras libraries and packages
class DNNModel:

    def __init__(self):
        self.model = None

    @staticmethod
    def shows_graphs(history):
        loss = history.history['loss']
        val_loss = history.history['val_loss']
        epochs = range(1, len(loss) + 1)
        plt.plot(epochs, loss, 'bo', label='Training loss')
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.xlabel('Epochs')
        plt.ylabel('Loss')
        plt.legend()
        plt.show()

        plt.clf()
        acc = history.history['acc']
        val_acc = history.history['val_acc']
        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.xlabel('Epochs')
        plt.ylabel('Accuracy')
        plt.legend()
        plt.show()

    @staticmethod
    def calculate_accuracy(predictions, test_data):
        value_results = pd.DataFrame(0, index=np.arange(len(test_data)), columns=["accuracy"])
        columns = [x for x in range(len(test_data[0]))]
        length = len(test_data)
        x = 0
        while x < length:
            values1 = predictions[x]
            values2 = test_data[x]
            tp = len([y for y in columns if values1[y] == 1 and values2[y] == 1])
            tn = len([y for y in columns if values1[y] == 0 and values2[y] == 0])
            fp = len([y for y in columns if values1[y] == 1 and values2[y] == 0])
            fn = len([y for y in columns if values1[y] == 0 and values2[y] == 1])
            value_results.loc[x] = (tp + tn) / (tp + tn + fp + fn)
            x += 1

        accuracy_values = value_results.accuracy.values.tolist()

        return (sum(accuracy_values) / len(accuracy_values))

    @staticmethod
    def preprocess_data(initial_table, user_test, list_categories):
        user_test_size = len(user_test)

        data_to_process = pd.concat([initial_table, user_test], ignore_index=True)

        categories_table = data_to_process[list_categories]

        # 1st step, use one hot enconding on the table
        result_cities = pd.get_dummies(data_to_process['geo_city'])
        result_continent = pd.get_dummies(data_to_process['geo_continent'])
        result_country = pd.get_dummies(data_to_process['geo_country'])
        result_persona_id = pd.get_dummies(data_to_process['personaIdScores_id'])
        result_global_persona_id = pd.get_dummies(data_to_process['globalPersonaIdScores_id'])
        users_table = data_to_process.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id',
                                                    'globalPersonaIdScores_id'])
        users_table = pd.concat([users_table, result_cities, result_continent, result_country, result_persona_id,
                                 result_global_persona_id], axis=1)

        # 2nd step, drop the labels
        to_drop = list_categories
        to_drop.extend(['categories', 'transactionPath', 'visitorId'])
        users_table = users_table.drop(columns=to_drop)

        # 3rd step, separate the unwanted rows to a new users table
        user_test_data = users_table.tail(user_test_size)

        # 4th step, separate the unwanted rows to a new categories table
        user_test_categories = categories_table.tail(user_test_size)

        # 5th step, remove the unwanted rows from the whole users data table
        users_table = users_table.drop(user_test_data.index.values.tolist())

        # 6th step, remove the unwanted rows from the whole categories table
        categories_table = categories_table.drop(user_test_categories.index.values.tolist())

        # 7th step, get the wanted input
        X = users_table.iloc[:, :].values
        X_visitors = user_test_data.iloc[:, :].values

        # 8nd step, get the wanted labels
        Y = categories_table.iloc[:, :].values
        Y_visitors = user_test_categories.iloc[:, :].values

        return X, Y, X_visitors, Y_visitors, users_table, categories_table, data_to_process

    def create_model(self, length_x, length_y):
        model = Sequential()
        model.add(Dense(32, activation='relu', input_shape=(length_x,)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(length_y, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model

        return model

    def train_model(self, X, Y, graphs=False):
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        history = self.model.fit(X_train, Y_train, epochs=4, batch_size=512, validation_data=(X_test, Y_test))

        if graphs:
            DNNModel.shows_graphs(history)


    def predict_values(self, input_x):
        prediction = self.model.predict(input_x)
        #prediction[prediction >= 0.5] = 1
        #prediction[prediction < 0.5] = 0

        return prediction

    @staticmethod
    def k_fold_validation(X, Y, length_x, length_y):
        dnn_model_val = DNNModel()
        kf = KFold(n_splits=10)
        scores = []
        for train_index, test_index in kf.split(X):
            print("TRAIN:", train_index, "TEST:", test_index)
            model = dnn_model_val.create_model(length_x, length_y)
            X_train, X_test = X[train_index], X[test_index]
            Y_train, Y_test = Y[train_index], Y[test_index]
            model.fit(X_train, Y_train, epochs=4, batch_size=512)
            scores.append(model.evaluate(X_test, Y_test))

        return scores