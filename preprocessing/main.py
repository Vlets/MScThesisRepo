from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles
import pandas as pd
import time
from kmodes.kmodes import KModes

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/bigdata.json"
processedData = '/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/finalDataDropped.json'

# THE ONE FUNCTION TO RULE THEM ALL IS do_it_all(filePath)
'''
start = time.time()
final_dataframe = jsonTools.do_it_all(filePath)
end = time.time()
print(end-start)

droplist = ['geo.latitude','geo.location.lat','geo.location.lon','geo.longitude',
            'journeypersona.terms','globalPersonaIdScores',
            'personaIdScores','audience.terms', 'categories.terms']
finaldf = final_dataframe.drop(droplist, axis=1)
'''
finaldf = jsonTools.json_read(processedData)
finaldf = finaldf.astype(str)

kmodes_huang = KModes(n_clusters=8, init='Huang', verbose=1)
start = time.time()
kmodes_huang.fit(finaldf)
end = time.time()
print(end-start)


column_names = list(finaldf.columns.values)
result = kmodes_huang.cluster_centroids_
clusters = pd.DataFrame(result, columns=column_names)

# TODO: TESTS TO CONFIRM RESULTS

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)

#df = jsonTools.json_read('/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/finalDataDropped.json')
#finaldf = df.astype(str)


