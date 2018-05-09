from preprocessing.helpers.JsonProcessor import JsonProcessor
import preprocessing.dataFiles.mockData as dataFiles

jsonTools = JsonProcessor()

filePath = "/Users/george/Expendable/data.json"

sortBy = ["visitorId", "timestamp"]
categoricalData = ["audience", "visitorId", "channel", "url", "geo", "newVisit"]


data = jsonTools.json_read(filePath)
sortedData = jsonTools.json_sort(data, sortBy)


# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)


