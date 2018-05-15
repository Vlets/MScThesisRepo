from preprocessing.helpers.JsonProcessor import JsonProcessor
from preprocessing.Joana.NormalizePersona import NormalizePersona

json_Tools = JsonProcessor()

sortedData = json_Tools.read_and_sort_data("./test2.json")
sortedData = sortedData.reset_index().drop('index', axis=1)


sortedData = NormalizePersona.normalize_table_personas(sortedData)