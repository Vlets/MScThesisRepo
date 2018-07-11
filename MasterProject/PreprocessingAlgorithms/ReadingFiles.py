import json
import pandas as pd
from sqlalchemy import create_engine


class ReadingFiles:

    def __init__(self):
        self.engine = None

    def connect_to_database(self, uri):
        # uri = 'mysql://root:123bloom@127.0.0.1/bloomdata'
        self.engine = create_engine(uri)

    def make_query(self, query):
        # 'SELECT entry FROM requestlog LIMIT 10'
        query = pd.read_sql(query, self.engine)
        return query

    @staticmethod
    def query_to_json_file(query, column, path_file):
        index = 0
        data_json = []

        while index < len(query):
            j = query.at[index, column]
            my_json = j.decode('utf8')
            data = json.loads(my_json)
            data_json.append(data)
            index += 1

        print("DONE 1")

        if path_file != "":
            with open(path_file, 'w') as outfile:
                json.dump(data_json, outfile, indent=0)

            print("DONE 2")

        else:
            return data_json
