from MasterProject.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from MasterProject.DataAlgorithms.NormalizePersona import NormalizePersona

json_Tools = JsonProcessor()

sortedData = json_Tools.json_files_pre_processing("./test_mb.json")



result_sortedData = NormalizePersona.normalize_table_personas(sortedData)