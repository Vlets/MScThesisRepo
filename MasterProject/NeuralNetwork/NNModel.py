from MasterProject.PreprocessingAlgorithms.PreprocessingData import PreprocessingData
from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Importing the Keras libraries and packages
class NNModel:

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

        return sum(accuracy_values) / len(accuracy_values)

    @staticmethod
    def split_users_data_and_keywords_data(initial_table, list_keywords):
        """
        This method separates the initial_table into two table, the users data
        and the keywords data
        :param initial_table: The table used to make the separation
        :param list_keywords: List with all values of keywords
        :return: Data of users; Data with keywords
        """

        keywords_table = initial_table[list_keywords]

        data_to_process = initial_table.drop(columns=list_keywords)

        to_drop = ['keywords', 'transactionPath', 'visitorId']
        data_to_process = data_to_process.drop(columns=to_drop)

        X = data_to_process.iloc[:, :].values

        Y = keywords_table.iloc[:, :].values

        return X, Y

    def create_model(self, length_x, length_y):
        """
        This method created the Neural Network model with the given dimensions
        fro the input layer and output layer
        :param length_x: Dimension fr the input layer
        :param length_y: Number of nodes for the output layer
        :return: A Neural Network model
        """
        model = Sequential()
        model.add(Dense(64, activation='relu', input_shape=(length_x,)))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(length_y, activation='sigmoid'))
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        self.model = model

        return model

    def train_model(self, X, Y, graphs=False):
        """
        This method trains the Neural Network with the given input and output data
        :param X: The input data
        :param Y: The output data
        :param graphs: If true, shows graphs regarding the loss and accuracy when
        training; otherwise, shows no graphs
        :return: Nothing, just trains the Neural Network
        """
        # Shuffle and split
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        if graphs:
            history = self.model.fit(X_train, Y_train, epochs=4, batch_size=512, validation_data=(X_test, Y_test))
            NNModel.shows_graphs(history)

        else:
            X_train = np.append(X_train, X_test, axis=0)
            Y_train = np.append(Y_train, Y_test, axis=0)
            self.model.fit(X_train, Y_train, epochs=4, batch_size=512, verbose=0)

    def predict_values(self, input_x):
        """
        This method makes a prediction based on the given data
        :param input_x: The given data to use to make a prediction
        :return: The prediction made with binary values
        """
        prediction = self.model.predict(input_x)
        prediction[prediction >= 0.47] = 1
        prediction[prediction < 0.47] = 0

        return prediction

    @staticmethod
    def k_fold_validation(X, Y, length_x, length_y):
        dnn_model_val = NNModel()
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
