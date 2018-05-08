from preprocessing.Joana.ReadingFiles import ReadingFiles as rf
import pandas as pd

uri = 'mysql://root:123bloom@127.0.0.1/bloomreachdatabase'

reading_files = rf()
reading_files.connect_to_database(uri)

query = 'SELECT entry FROM requestlog LIMIT 4470605'
#query = 'SELECT entry FROM requestlog ORDER BY requestTime DESC LIMIT 1;'

query_result = reading_files.make_query(query)

reading_files.query_to_json_file(query_result, 'entry', './test2.json')
