from preprocessing.JsonProcessor import JsonProcessor

jsonTools = JsonProcessor()

filePath = "/Users/george/Expendable/sample.json"

sortBy = ["visitorId", "timestamp"]

data = jsonTools.json_read(filePath)
sortedData = jsonTools.json_sort(data, sortBy)

# Save to Json
jsonTools.json_save(sortedData, "./testProduced.json")
