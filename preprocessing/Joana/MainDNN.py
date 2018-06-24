from preprocessing.Joana.PreprocessingData import PreprocessingData
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.models import Sequential
from keras.layers import Dense
import matplotlib.pyplot as plt
import pandas as pd
# Importing the Keras libraries and packages


#SIZE WHICH IT WORKS ----->
#values_size = math.ceil((len(sortedData))/56)

sortedData = pd.read_json("./processed_table_3.json")
list_categories = PreprocessingData.create_categories_list(sortedData, 'categories')
sortedData = sortedData.reset_index(drop=True)

categories_table = sortedData[list_categories]
sortedData['null'] = sortedData.null.apply(lambda x: x if pd.notna(x) else 0.0)

#1st step, turn columns into strings
sortedData['geo_city'] = sortedData['geo_city'].astype(str)
sortedData['geo_continent'] = sortedData['geo_continent'].astype(str)
sortedData['geo_country'] = sortedData['geo_country'].astype(str)

#2nd step, chose the "labels"
#Y = sortedData.iloc[:, 6:8].values
#result_global_id = pd.get_dummies(sortedData['globalPersonaIdScores_id'])
Y = categories_table.iloc[:, :].values

#3rd step, drop the labels
list_to_drop = list_categories
list_to_drop.extend(['categories'])
sortedData = sortedData.drop(columns=list_to_drop)

#4th step, use one hot enconding on the table
result_cities = pd.get_dummies(sortedData['geo_city'])
result_continent = pd.get_dummies(sortedData['geo_continent'])
result_country = pd.get_dummies(sortedData['geo_country'])
result_persona_id = pd.get_dummies(sortedData['personaIdScores_id'])
result_global_persona_id = pd.get_dummies(sortedData['globalPersonaIdScores_id'])
#sortedData = sortedData.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id',
#                                      'globalPersonaIdScores_id'])
testing_table = sortedData.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id',
                                         'globalPersonaIdScores_id'])
testing_table = pd.concat([testing_table, result_cities, result_continent, result_country, result_persona_id,
                        result_global_persona_id], axis=1)

#5th step, get the wanted input
X = testing_table.iloc[:, :].values

#6th step, label encoder on binary value columns
#labelencoder_1 = LabelEncoder()
#labelencoder_2 = LabelEncoder()
#X[:,1] = labelencoder_1.fit_transform(X[:,1])
#X[:,3] = labelencoder_2.fit_transform(X[:,3])

#7th step, encode the label

#8th step. split the dataset into the training set and test set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2)

length_x = len(testing_table.columns.values.tolist())
length_y = len(categories_table.columns.values.tolist())

sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""X_train = X[:8982]
X_test = X[8982:]

Y_train = Y[:8982]
Y_test = Y[8982:]

X_val = X_train[:1000]
partial_x_train = X_train[1000:]

Y_val = Y_train[:1000]
partial_y_train = Y_train[1000:]"""



#9th step initializing Deep Neural Network
model = Sequential()
model.add(Dense(64, activation='relu', input_shape=(length_x,)))
model.add(Dense(64, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dense(length_y, activation='sigmoid'))
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

#10th step, training the model
history = model.fit(X_train,
                    Y_train,
                    epochs=20,
                    batch_size=512,
                    validation_data=(X_test, Y_test))

results = model.evaluate(X_test, Y_test)

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

