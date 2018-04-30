import pandas as pd


class JsonProcessing:

    def json_read(self, filepath):
        self.file = pd.read_json(filepath, lines=True, convert_dates=False)
        return self.file

    def json_sort(self, file):
        sortedfile = file.sort_values(by=["visitorId", "timestamp"])
        return sortedfile

    def json_save(self, sorteddata, savepath):
        sorteddata.to_json(savepath)