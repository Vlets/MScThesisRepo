import time
import pandas as pd
from segmentation.helpers.JsonProcessor import JsonProcessor
from segmentation.helpers import urlKeywordExtractor as urlExtract


jsonTools = JsonProcessor()

bigData = "/Users/george/PycharmProjects/scikitLiterallyLearn/segmentation/dataFiles/bigdata.json"

# THE ONE FUNCTION TO RULE THEM ALL IS pipeline(filePath)

clusters = jsonTools.pipeline(bigData)

# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
# jsonTools.json_save(sortedData, "./dataFiles/testProduced", toJson=False)

