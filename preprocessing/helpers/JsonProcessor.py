import pandas as pd
from pandas.io.json import json_normalize


class JsonProcessor:

    def json_read(self, filepath, multiline=False):
        file = pd.read_json(filepath, lines=multiline, convert_dates=False)
        return file

    def json_sort(self, file, sort_by):
        if isinstance(sort_by, list):
            sorted_file = file.sort_values(by=sort_by)
            return sorted_file
        raise ValueError("sort_by should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    def json_save(self, sorted_data, savepath, to_json=True):
        if to_json:
            sorted_data.to_json(savepath + ".json", force_ascii=False)
        if not to_json:
            sorted_data.to_csv(savepath + ".csv")

    def normalize_collectors(self, data_frame):
        collector_data = json_normalize(data_frame['collectorData'])
        all_data = pd.concat([collector_data, data_frame], axis=1)
        processed_data = all_data.drop(['collectorData'], axis=1)
        return processed_data

    def do_it_all(self, file_path):
        sort_by = ["visitorId", "timestamp"]
        data_frame = self.json_read(file_path)
        processed_data = self.normalize_collectors(data_frame)
        sorted_data = self.json_sort(processed_data, sort_by)
        return sorted_data
