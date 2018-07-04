import pandas as pd
from kmodes.kmodes import KModes
from pandas.io.json import json_normalize
from segmentation.helpers import urlKeywordExtractor as urlExtract
from segmentation.dataAlgorithms.MFAlgorithm import MFAlgorithm as mfa


class JsonProcessor:

    # Step 1
    def json_read(self, filepath, multiline=False):
        file = pd.read_json(filepath, lines=multiline, convert_dates=False)
        print("Step 1/7 - Reading, done...")
        return file

    # Step 2
    # Keep list defines all the columns to be kept in the pipeline. All others are dropped.
    def filter_columns(self, data_frame):
        collector_data = json_normalize(data_frame['collectorData'])
        all_data = pd.concat([collector_data, data_frame], axis=1)
        keep_list = ['visitorId', 'timestamp', 'pageUrl',
                     'newVisit', 'pageId']
        processed_data = all_data[keep_list]
        print("Step 2/7 - Filtering, done...")
        return processed_data

    # Step 3
    def json_sort(self, file):
        sort_by = ["visitorId", "timestamp"]
        sorted_file = file.sort_values(by=sort_by)
        print("Step 3/7 - Sorting, done...")
        return sorted_file

    # Step 4
    def get_transactions(self, sorted_data):
        transactions = mfa.init_algorithm(sorted_data)
        data_frame = pd.DataFrame(transactions, columns=['visitorId', 'timestamp', 'transactionPath'])
        data_frame = pd.merge(data_frame, sorted_data, on=['visitorId', 'timestamp'])
        print("Step 4/7 - Extract transactions, done...")
        return data_frame.drop(['timestamp', 'pageUrl'], axis=1)

    # Step 5
    def get_content_page_and_keywords(self, data_frame):
        data_frame['keywords'] = data_frame.transactionPath.astype(str).apply(urlExtract.get_keywords)
        data_frame['contentPage'] = data_frame.transactionPath.str[-1]
        print("Step 5/7 - Keep content pages and get path keywords, done...")
        return data_frame

    # Step 6
    # This step would require the login and home URLs to be provided by the user.
    def remove_homepage(self, data_frame):
        data_frame = data_frame.drop(
            data_frame[(
                        (data_frame.pageId == 'hst:pages/home') |
                        (data_frame.pageId == 'hst:pages/pagenotfound')
                       )
                       &
                       (data_frame.transactionPath.str.len() == 1)
                       ].index).reset_index(drop=True)
        print("Step 6/7 - Remove visitors that only visited the homepage, done...")
        return data_frame

    # Step 7
    def cluster_data(self, data_frame, number_of_segments=10):
        data_frame = data_frame.astype(str)
        kmodes_cao = KModes(n_clusters=number_of_segments, init='Cao', verbose=1)
        kmodes_cao.fit_predict(data_frame)

        column_names = list(data_frame.columns.values)
        clusters = pd.DataFrame(kmodes_cao.cluster_centroids_, columns=column_names)
        print("Step 7/7 - Clustering, done...")
        return clusters

# ---------------Combinations of steps for ease of testing------------------

    # Steps 1-3 combined
    def read_and_sort_data(self, file_path):
        data_frame = self.json_read(file_path)
        processed_data = self.filter_columns(data_frame)
        sorted_data = self.json_sort(processed_data)
        return sorted_data.reset_index(drop=True)

    # Steps 4-6
    def pre_process(self, data_frame):
        data_frame = self.get_transactions(data_frame)
        data_frame = data_frame.drop('visitorId', axis=1)
        data_frame = self.get_content_page_and_keywords(data_frame)
        data_frame = self.remove_homepage(data_frame)
        data_frame = data_frame.drop(['transactionPath', 'pageId'], axis=1)
        return data_frame

    # All steps
    def segmentation_pipeline(self, file_path, number_of_segments=10):
        data_frame = self.read_and_sort_data(file_path)
        data_frame = self.pre_process(data_frame)
        clusters = self.cluster_data(data_frame, number_of_segments)
        print("Finished.")
        return clusters

    # Save to json or csv
    def json_save(self, sorted_data, savepath, to_json=True):
        if to_json:
            sorted_data.to_json(savepath + ".json", force_ascii=False)
        if not to_json:
            sorted_data.to_csv(savepath + ".csv")
