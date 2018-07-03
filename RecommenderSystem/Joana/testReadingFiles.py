from RecommenderSystem.PreprocessingAlgorithms.ReadingFiles import ReadingFiles as rf
from RecommenderSystem.PreprocessingAlgorithms.PreprocessingData import PreprocessingData

uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

reading_files = rf()
reading_files.connect_to_database(uri)

query = 'SELECT entry FROM requestlog LIMIT 6054'
#query2 = 'SELECT visitorData FROM visitors LIMIT 10'
#query = 'SELECT entry FROM requestlog ORDER BY requestTime DESC LIMIT 1;'

query_result = reading_files.make_query(query)
#query_result2 = reading_files.make_query(query2)

reading_files.query_to_json_file(query_result, 'entry',
                                 "/Users/Joana/Documents/GitHub/scikitLiterallyLearn/RecommenderSystem/FilesToTest/bloomreach_targeting_7mb.json")
#result = reading_files.query_to_json_file(query_result2, 'visitorData', "")

#pre_data = PreprocessingData()
#pre_data.preprocessing_DNN("./test3.json")