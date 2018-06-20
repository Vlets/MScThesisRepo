import numpy as np

class MFAlgorithm:

    @staticmethod
    def remove_duplicates(duplicate):
        final_list = []
        for num in duplicate:
            if num not in final_list:
                final_list.append(num)
        return final_list

    @staticmethod
    def categories_value(dict_path_categories, string):
        size_dict = len(dict_path_categories)
        count_nan = list(dict_path_categories.values()).count(np.nan)
        if size_dict > 1 and count_nan == size_dict:
            categories = np.nan
        elif size_dict > 1 and count_nan != size_dict:
            categories = [dict_path_categories[x] for x in string if isinstance(dict_path_categories[x], list)]
            categories = [item for sublist in categories for item in sublist]
            categories = MFAlgorithm.remove_duplicates(categories)
        else:
            categories = list(dict_path_categories.values())[0]

        return categories

    @staticmethod
    def run_MF_algorithm(visitor, time, path, dict_path_categories):
        tuples = [('', path[0], 0, 0)]
        i = 0
        path_size = len(path)
        while (i + 1) < path_size:
            tuples.append((path[i], path[i + 1], i, i+1))
            i += 1

        i = 0
        string = []
        flag = 1
        result = []
        timestamp = time[0]
        tuples_size = len(tuples)

        while i < tuples_size:
            varA, varB, indexA, indexB = tuples[i]

            if varA == '':
                if string:
                    if string not in result:
                        categories = MFAlgorithm.categories_value(dict_path_categories, string)
                        result.append((visitor, timestamp, string, categories))
                string.append(varB)
                timestamp = time[indexB]
                i += 1
                continue

            if varB in string:
                if flag == 1:
                    if string not in result:
                        categories = MFAlgorithm.categories_value(dict_path_categories, string)
                        result.append((visitor, timestamp, string, categories))
                index = string.index(varB)
                string = string[0:index + 1]
                flag = 0
                i += 1
                continue

            else:
                if flag == 0:
                    flag = 1
                    timestamp = time[indexA]
                string.append(varB)


            i += 1

        if string not in result:
            categories = MFAlgorithm.categories_value(dict_path_categories, string)
            result.append((visitor, timestamp, string, categories))

        return result

    @staticmethod
    def init_algorithm(sortedData):
        result = []
        grouped = sortedData.groupby('visitorId')
        i = 0
        visitor_length = len(grouped)
        print("Initializing Transaction Extraction...")
        for visitorId, group in grouped:
            time = grouped.get_group(visitorId).timestamp.tolist()
            path = grouped.get_group(visitorId).pageUrl.tolist()
            categories = grouped.get_group(visitorId).categories_terms.tolist()
            dict_path_categories = dict(zip(path, categories))
            result_paths = MFAlgorithm.run_MF_algorithm(visitorId, time, path, dict_path_categories)
            result.extend(result_paths)
            i += 1
            if i % 100 == 0:
                print("Progress:", round((i / visitor_length) * 100, 2), "%")
        return result