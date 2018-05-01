import pandas as pd
from sqlalchemy import create_engine


uri = 'mysql://root:123bloom@127.0.0.1/bloomdata'
engine = create_engine(uri)
sql_file = pd.read_sql('SELECT entry FROM requestlog LIMIT 1', engine)

print(sql_file)

sql_file.to_json("./test.json")
json_read = pd.read_json("test.json")

print(json_read)