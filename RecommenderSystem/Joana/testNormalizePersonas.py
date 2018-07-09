from RecommenderSystem.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from RecommenderSystem.DataAlgorithms.NormalizePersona import NormalizePersona

json_Tools = JsonProcessor()

sortedData = json_Tools.json_files_pre_processing("./test_mb.json")



result_sortedData = NormalizePersona.normalize_table_personas(sortedData)