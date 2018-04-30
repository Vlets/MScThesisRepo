from preprocessing.JsonProcessing import JsonProcessing

iWantToSort = JsonProcessing()

# Insert your Json file path
filePath = "/Users/george/Expendable/sample.json"

data = iWantToSort.json_read(filePath)
sortedData = iWantToSort.json_sort(data)

# Save to Json
iWantToSort.json_save(sortedData, "./testProduced.json")
