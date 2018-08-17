from sklearn.model_selection import KFold
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras import backend as K
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tensorflow as tf
import keras_metrics
from keras.callbacks import EarlyStopping


# Importing the Keras libraries and packages
class NNModel:

    def __init__(self):
        self.model = None
        self.threshold = None

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
        acc = history.history['precision']
        val_acc = history.history['val_precision']
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

    @staticmethod
    def as_keras_metric(method):
        import functools
        from keras import backend as K
        import tensorflow as tf
        @functools.wraps(method)
        def wrapper(self, args, **kwargs):
            """ Wrapper for turning tensorflow metrics into keras metrics """
            value, update_op = method(self, args, **kwargs)
            K.get_session().run(tf.local_variables_initializer())
            with tf.control_dependencies([update_op]):
                value = tf.identity(value)
            return value

        return wrapper

    @staticmethod
    def precision(y_true, y_pred):
        """Precision metric.
         Only computes a batch-wise average of precision.
         Computes the precision, a metric for multi-label classification of
        how many selected items are relevant.
        """
        true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
        predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
        precision = true_positives / (predicted_positives + K.epsilon())

        return precision

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
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=[
            keras_metrics.precision(),
            'accuracy'
        ])
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
        # X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        if graphs:
            early_stopping_accuracy = EarlyStopping(monitor='val_acc', min_delta=0.00001, patience=2, verbose=0,
                                                    mode='auto')
            early_stopping_precision = EarlyStopping(monitor='val_precision', min_delta=0.00001, patience=2, verbose=0,
                                                     mode='max')  # FOR PRECISION
            history = self.model.fit(X, Y, epochs=20, batch_size=512, shuffle=True, validation_split=0.2,
                                     callbacks=[
                                         early_stopping_accuracy,
                                         early_stopping_precision
                                     ])
            NNModel.shows_graphs(history)

        else:
            # train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size=0.2)
            self.model.fit(X, Y, epochs=12, batch_size=512, verbose=0, shuffle=True)
            # self.calculate_threshold(test_x, test_y)

    def predict_values(self, input_x):
        """
        This method makes a prediction based on the given data
        :param input_x: The given data to use to make a prediction
        :return: The prediction made with binary values
        """
        prediction = self.model.predict(input_x)
        top_values = sorted(prediction[0].tolist(), reverse=True)[:150]
        for val in top_values:
            prediction[prediction == val] = 1

        prediction[~(prediction == 1)] = 0

        return prediction

    @staticmethod
    def k_fold_validation(X, Y, length_x, length_y):
        nn_model_val = NNModel()
        kf = KFold(n_splits=10)
        scores = []
        for train_index, test_index in kf.split(X):
            print("TRAIN:", train_index, "TEST:", test_index)
            model = nn_model_val.create_model(length_x, length_y)
            train_x, test_x = X[train_index], X[test_index]
            train_y, test_y = Y[train_index], Y[test_index]
            model.fit(train_x, train_y, epochs=4, batch_size=512)
            scores.append(model.evaluate(test_x, test_y))

        return scores

    def calculate_threshold(self, test_x, test_y):
        predictions = self.model.predict(test_x)
        predictions_as_table = pd.DataFrame(predictions)
        actual_output = pd.DataFrame(test_y)
        result = []

        for index, row in actual_output.iterrows():
            t = actual_output.loc[index, (actual_output != 0).any(axis=0)]
            p = predictions_as_table.loc[index]
            inter = t[t == 1]
            value_indexes = inter.index.values.tolist()
            prediction_values = p[value_indexes].values.tolist()
            average = sum(prediction_values)/len(prediction_values)
            result.append(average)

        self.threshold = float("{:1.2f}".format(sum(result)/len(result)))
