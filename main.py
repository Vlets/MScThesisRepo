import pandas as pd
from pandas.io.json import json_normalize
import json

path = "/Users/george/Expendable/gaming.json"
path2 = "/Users/george/Expendable/sampleSmall.json"
path3 = "/Users/george/Expendable/sample.json"

dataset = pd.read_json(path3, lines=True, convert_dates=False)

sortedData = dataset.sort_values(by=["visitorId", "timestamp"])
sortedData.to_json("/Users/george/Expendable/sample_sort.json")

# sortedData.loc[sortedData['visitorId'] == '00329289-e63b-4bdb-9bb8-2da62161c353']
