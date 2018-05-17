from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles
import time
import tqdm

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/bigdata.json"


# THE ONE FUNCTION TO RULE THEM ALL IS do_it_all(filePath)

start = time.time()
final_dataframe = jsonTools.do_it_all(bigData)
end = time.time()
print(end-start)

# TODO: TESTS TO CONFIRM RESULTS

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)
