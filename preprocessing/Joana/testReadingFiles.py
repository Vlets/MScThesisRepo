from preprocessing.Joana.ReadingFiles import ReadingFiles as rf

uri = 'mysql://root:123bloom@127.0.0.1/bloomdata'

reading_files = rf()
reading_files.connect_to_database(uri)

query = 'SELECT entry FROM requestlog LIMIT 10'

query_result = reading_files.make_query(query)

reading_files.query_to_json_file(query_result, 'entry', './test.json')