from preprocessing.helpers.JsonProcessor import JsonProcessor
from preprocessing.dataAlgorithms.NormalizePersona import NormalizePersona
from preprocessing.dataAlgorithms.ReadingFiles import ReadingFiles as rf
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import pandas as pd

# Importing the Keras libraries and packages

def remove_duplicates(duplicate):
    final_list = []
    for num in duplicate:
        if num not in final_list:
            final_list.append(num)
    return final_list

def create_categories_list(items_table):
    list_categories = [x for x in items_table.categories_terms.values.tolist() if str(x) != 'nan']
    categories = [item for sublist in list_categories for item in sublist]
    categories = remove_duplicates(categories)
    return categories


def sublist(lst1, lst2):
    ls1 = [element for element in lst1 if element in lst2]
    ls2 = [element for element in lst2 if element in lst1]

    if ls1 == ls2:
        return []
    else:
        return lst1

def useless_function(lst1):
    return sublist(lst1, list_categories)


uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

json_Tools = JsonProcessor()

reading_files = rf()
reading_files.connect_to_database(uri)


sortedData = json_Tools.do_it_all("./test_mb.json")
#sortedData.to_json("./test2_processed.json")

#sortedData = pd.read_json("./test2_processed_personas.json")
#sortedData = sortedData.reset_index(drop=True)
#sortedData = sortedData.drop(columns=['referer', 'audience.terms', 'categories.terms', 'userAgent', 'visitorId'])

sortedData = NormalizePersona.normalize_table_personas(sortedData)
#sortedData.to_json("./test2_processed_personas.json")

items_table = json_Tools.make_items_table()
list_categories = create_categories_list(items_table)
sortedData = sortedData[pd.notna(sortedData['categories'])]
sortedData = sortedData.reset_index(drop=True)
sortedData['categories'] = sortedData.categories.apply(useless_function)
sortedData = sortedData[sortedData.astype(str)['categories'] != '[]']


#result = pd.get_dummies(sortedData, columns=['geo.city'])

#sortedData.visitorId.to_sql("VISITORSID", reading_files.engine, if_exists='replace')

#query = 'SELECT visitorId, visitorData FROM visitors WHERE visitorId IN (SELECT visitorId FROM VISITORSID)'
#result = reading_files.make_query(query)

#data_frame_result = json_normalize(reading_files.query_to_json_file(result, 'visitorData', ""))


#SIZE WHICH IT WORKS ----->
"""#values_size = math.ceil((len(sortedData))/56)

#1st step, turn columns into strings
sortedData['geo_city'] = sortedData['geo_city'].astype(str)
sortedData['geo_continent'] = sortedData['geo_continent'].astype(str)
sortedData['geo_country'] = sortedData['geo_country'].astype(str)

#2nd step, chose the "labels"
#Y = sortedData.iloc[:, 6:8].values
result_global_id = pd.get_dummies(sortedData['globalPersonaIdScores_id'])
Y = result_global_id.iloc[:, :].values

#3rd step, drop the labels
sortedData = sortedData.drop(columns=['globalPersonaIdScores_id', 'transactionPath'])

#4th step, use one hot enconding on the table
result_cities = pd.get_dummies(sortedData['geo_city'])
result_continent = pd.get_dummies(sortedData['geo_continent'])
result_country = pd.get_dummies(sortedData['geo_country'])
result_persona_id = pd.get_dummies(sortedData['personaIdScores_id'])
sortedData = sortedData.drop(columns=['geo_city', 'geo_continent', 'geo_country', 'personaIdScores_id'])
sortedData = pd.concat([sortedData, result_cities, result_continent, result_country, result_persona_id], axis=1)

#5th step, get the wanted input
X = sortedData.iloc[:, :].values

#6th step, label encoder on binary value columns
labelencoder_1 = LabelEncoder()
labelencoder_2 = LabelEncoder()
X[:,1] = labelencoder_1.fit_transform(X[:,1])
X[:,3] = labelencoder_2.fit_transform(X[:,3])

#7th step, encode the label

#8th step. split the dataset into the training set and test set
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = 0.2)

#9th step initializing Deep Neural Network
#model = Sequential()
#model.add(Dense(100, activation='relu', input_shape=(11306,)))
#model.add(Dense(100, activation='relu'))
#model.add(Dense(100, activation='relu'))
#model.add(Dense(100, activation='relu'))
#model.add(Dense(100, activation='relu'))
#model.add(Dense(100, activation='relu'))
#model.add(Dense(11, activation='softmax'))
#model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

#10th step, training the model
#history = model.fit(X_train,
#                    Y_train,
#                    epochs=20,
#                    batch_size=100
#                    validation_data = (X_test, Y_test))
#
"""