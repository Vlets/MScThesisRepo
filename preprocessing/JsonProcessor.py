import pandas as pd


class JsonProcessor:

    def json_read(self, filepath):
        self.file = pd.read_json(filepath, lines=True, convert_dates=False)
        return self.file

    def json_sort(self, file, sortby):
        if isinstance(sortby, list):
            sortedfile = file.sort_values(by=sortby)
            return sortedfile
        raise ValueError("sortby should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    def json_save(self, sorteddata, savepath):
        sorteddata.to_json(savepath, force_ascii=False)