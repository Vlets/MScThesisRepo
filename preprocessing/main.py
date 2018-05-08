from preprocessing.JsonProcessor import JsonProcessor
import pandas as pd
import numpy as np
from kmodes.kprototypes import KPrototypes
from pandas.io.json import json_normalize

jsonTools = JsonProcessor()

filePath = "/Users/george/Expendable/data.json"

sortBy = ["visitorId", "timestamp"]
categoricalData = ["audience", "visitorId", "channel", "url", "geo", "newVisit"]


data = jsonTools.json_read(filePath)
sortedData = jsonTools.json_sort(data, sortBy)


# Save to Json/CSV. If you don't want to specify a path, simply put the filename.
jsonTools.json_save(sortedData, "./testProduced", toJson=False)


