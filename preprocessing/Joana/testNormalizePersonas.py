from preprocessing.helpers.JsonProcessor import JsonProcessor
from preprocessing.dataAlgorithms.NormalizePersona import NormalizePersona

json_Tools = JsonProcessor()

sortedData = json_Tools.do_it_all("./test_mb.json")



result_sortedData = NormalizePersona.normalize_table_personas(sortedData)