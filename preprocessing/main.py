from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles


jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/preprocessing/dataFiles/test2.json"


data = jsonTools.do_it_all(filePath)

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)
