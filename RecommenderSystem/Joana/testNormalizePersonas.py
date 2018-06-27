from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from RecommenderSystem.DataAlgorithms.NormalizePersona import NormalizePersona

json_Tools = JsonProcessor()

sortedData = json_Tools.do_it_all("./test_mb.json")



result_sortedData = NormalizePersona.normalize_table_personas(sortedData)