from pandas.io.json import json_normalize
from MasterProject.PreprocessingAlgorithms.JsonProcessor import JsonProcessor
from MasterProject.DataAlgorithms.NormalizePersona import NormalizePersona
from MasterProject.PreprocessingAlgorithms.ReadingFiles import ReadingFiles as rf

uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

json_Tools = JsonProcessor()

reading_files = rf()
reading_files.connect_to_database(uri)


sortedData = json_Tools.json_files_pre_processing("./test_mb.json")
sortedData = NormalizePersona.normalize_table_personas(sortedData)

user_index = 167
user_id = sortedData.visitorId[user_index]
user_id_sql = "'" + user_id + "'"

query = 'SELECT visitorData FROM visitors WHERE visitorId = ' + user_id_sql

result = reading_files.make_query(query)
data_frame_result = reading_files.query_to_json_file(result, 'visitorData', "")[0]

user_persona = sortedData[sortedData['visitorId'] == user_id]['globalPersonaIdScores_id'].get(user_index)

if user_persona == 'None':
    user_persona = sortedData[sortedData['visitorId'] == user_id]['personaIdScores_id'].get(user_index)

user_characteristics = json_normalize(data_frame_result['data'])

user_paths = sortedData[sortedData['visitorId'] == user_id].transactionPath

persona_paths = sortedData[sortedData['globalPersonaIdScores_id'] == user_persona]

persona_paths.visitorId.to_sql("VISITORSID", reading_files.engine, if_exists='replace')

query2 = 'SELECT visitorData FROM visitors WHERE visitorId IN (SELECT visitorId FROM VISITORSID)'
result_query2 = reading_files.make_query(query2)

persona_characteristics = json_normalize(reading_files.query_to_json_file(result_query2, 'visitorData', ""))

persona_paths = persona_paths.transactionPath
