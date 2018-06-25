from preprocessing.helpers.PreprocessingData import PreprocessingData
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
    def preprocess_data(file):
        data_to_process = pd.read_json(file)

        list_categories = PreprocessingData.create_categories_list(data_to_process, 'categories')
        data_to_process = data_to_process.reset_index(drop=True)

        categories_table = data_to_process[list_categories]
        data_to_process['null'] = data_to_process.null.apply(lambda x: x if pd.notna(x) else 0.0)

        # 1st step, turn columns into strings
        data_to_process['geo_city'] = data_to_process['geo_city'].astype(str)
        data_to_process['geo_continent'] = data_to_process['geo_continent'].astype(str)
        data_to_process['geo_country'] = data_to_process['geo_country'].astype(str)

        # 2nd step, chose the "labels"
        Y = categories_table.iloc[:, :].values

        # 3rd step, drop the labels
        list_categories.extend(['categories'])
        data_to_process = data_to_process.drop(columns=list_categories)

        # 4th step, use one hot enconding on the table
        result_cities = pd.get_dummies(data_to_process['geo_city'])
        result_continent = pd.get_dummies(data_to_process['geo_continent'])
        result_country = pd.get_dummies(data_to_process['geo_country'])
        result_persona_id = pd.get_dummies(data_to_process['personaIdScores_id'])
        result_global_persona_id = pd.get_dummies(data_to_process['globalPersonaIdScores_id'])
        users_table = data_to_process.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id',
                                                    'globalPersonaIdScores_id'])
        users_table = pd.concat([users_table, result_cities, result_continent, result_country, result_persona_id,
                                 result_global_persona_id], axis=1)

        # 5th step, get the wanted input
        X = users_table.iloc[:, :].values


        return X, Y, users_table, categories_table, data_to_process


    def create_model(self, length_x, length_y):
        model = Sequential()
        model.add(Dense(32, activation='relu', input_shape=(length_x,)))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(length_y, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model

        return model


    def train_model(self, X, Y, graphs=False):
        #X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)

        X_train = X[:8982]
        X_test = X[8982:]

        Y_train = Y[:8982]
        Y_test = Y[8982:]

        X_val = X_train[:1000]
        partial_x_train = X_train[1000:]

        Y_val = Y_train[:1000]
        partial_y_train = Y_train[1000:]

        history = self.model.fit(partial_x_train,
                                 partial_y_train,
                                 epochs=10,
                                 batch_size=512,
                                 validation_data=(X_val, Y_val))

        results = self.model.evaluate(X_test, Y_test)

        predictions = self.model.predict(X_test)
        predictions[predictions >= 0.5] = 1
        predictions[predictions < 0.5] = 0


        final_result = DNNModel.calculate_accuracy(predictions, Y_test)

        if graphs:
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
            plt.ylabel('Loss')
            plt.legend()
            plt.show()

        return results, predictions, final_result


    def predict_values(self, input):
        return self.model.predict(input)

