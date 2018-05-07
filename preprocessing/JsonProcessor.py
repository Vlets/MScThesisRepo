import pandas as pd


class JsonProcessor:

    def json_read(self, filepath):
        file = pd.read_json(filepath, lines=False, convert_dates=False)
        return file

    def json_sort(self, file, sortby):
        if isinstance(sortby, list):
            sortedfile = file.sort_values(by=sortby)
            return sortedfile
        raise ValueError("sortby should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    def json_save(self, sorteddata, savepath, toJson = True):
        if toJson:
            sorteddata.to_json(savepath + ".json", force_ascii=False)
        if not toJson:
            sorteddata.to_csv(savepath + ".csv")
