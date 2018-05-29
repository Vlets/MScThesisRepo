import pandas as pd
from pandas.io.json import json_normalize
from segmentation.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa
from kmodes.kmodes import KModes


class JsonProcessor:

    # Step 1
    def json_read(self, filepath, multiline=False):
        file = pd.read_json(filepath, lines=multiline, convert_dates=False)
        print("Step 1/6 - Reading, done...")
        return file

    # Step 2
    def filter_columns(self, data_frame):
        collector_data = json_normalize(data_frame['collectorData'])
        all_data = pd.concat([collector_data, data_frame], axis=1)
        keep_list = ['visitorId', 'timestamp', 'pageUrl', 'geo.country',
                     'returningvisitor', 'newVisit', 'referer', 'userAgent']
        processed_data = all_data[keep_list]
        print("Step 2/6 - Filtering, done...")
        return processed_data

    # TODO:  When finished, remove sortBy and the typecheck. Sort by id + timestamp.
    # Step 3
    def json_sort(self, file, sort_by):
        if isinstance(sort_by, list):
            sorted_file = file.sort_values(by=sort_by)
            print("Step 3/6 - Sorting, done...")
            return sorted_file
        raise ValueError("sort_by should be a list indicating column keys: [\"col1\", \"col2\", ...]")

    # Step 4
    def get_transactions(self, sorted_data):
        transactions = mfa.init_algorithm(sorted_data)
        data_frame = pd.DataFrame(transactions, columns=['visitorId', 'timestamp', 'transactionPath'])
        data_frame = pd.merge(data_frame, sorted_data, on=['visitorId', 'timestamp'])
        print("Step 4/6 - Extract transactions, done...")
        return data_frame.drop(['timestamp', 'pageUrl'], axis=1)

    # Step 5
    def remove_homepage_and_stringify(self, data_frame):
        data_frame = data_frame.astype(str)
        homepages = ["[\'https://www.onehippo.com/en\']", "[\'https://www.onehippo.org/\']"]
        for homepage in homepages:
            data_frame = data_frame[data_frame.transactionPath != homepage]
        print("Step 5/6 - Remove visitors that only visited the homepage, done...")
        return data_frame

    # Step 6
    def cluster_data(self, data_frame, number_of_segments=17):
        kmodes_cao = KModes(n_clusters=number_of_segments, init='Cao', verbose=1)
        kmodes_cao.fit(data_frame)

        column_names = list(data_frame.columns.values)
        clusters = pd.DataFrame(kmodes_cao.cluster_centroids_, columns=column_names)
        print("Step 6/6 - Clustering, done...")
        return clusters

    # Steps 1-3 combined
    def read_and_sort_data(self, file_path):
        sort_by = ["visitorId", "timestamp"]
        data_frame = self.json_read(file_path)
        processed_data = self.filter_columns(data_frame)
        sorted_data = self.json_sort(processed_data, sort_by)
        return sorted_data.reset_index(drop=True)

    # Steps 1-4
    def pre_process(self, file_path):
        data_frame = self.read_and_sort_data(file_path)
        data_frame = self.get_transactions(data_frame)
        return data_frame

    # All steps
    def pipeline(self, file_path, number_of_segments=17):
        data_frame = self.pre_process(file_path)
        data_frame = self.remove_homepage_and_stringify(data_frame)
        data_frame = data_frame.drop('visitorId', axis=1)
        clusters = self.cluster_data(data_frame, number_of_segments)
        print("Finished.")
        return clusters

    # Save to json or csv
    def json_save(self, sorted_data, savepath, to_json=True):
        if to_json:
            sorted_data.to_json(savepath + ".json", force_ascii=False)
        if not to_json:
            sorted_data.to_csv(savepath + ".csv")
