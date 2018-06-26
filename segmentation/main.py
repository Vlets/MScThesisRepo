from segmentation.helpers.JsonProcessor import JsonProcessor

jsonTools = JsonProcessor()

filePath = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/test2.json"
bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"

# THE ONE FUNCTION TO RULE THEM ALL IS pipeline(filePath)

clusters = jsonTools.pipeline(filePath, 26)

