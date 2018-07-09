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
    def keywords_value(dict_url_keywords, string):
        size_dict = len(dict_url_keywords)
        count_nan = list(dict_url_keywords.values()).count(np.nan)
        if 1 < size_dict == count_nan:
            keywords = np.nan
        elif 1 < size_dict != count_nan:
            keywords = [dict_url_keywords[x] for x in string if isinstance(dict_url_keywords[x], list)]
            keywords = [item for sublist in keywords for item in sublist]
            keywords = MFAlgorithm.remove_duplicates(keywords)
        else:
            keywords = list(dict_url_keywords.values())[0]

        return keywords

    @staticmethod
    def run_MF_algorithm(visitor, time, urls, dict_urls_keywords):
        """

        :param visitor:
        :param time:
        :param urls:
        :param dict_urls_keywords:
        :return:
        """
        url_pairs = [('', urls[0], 0, 0)]
        i = 0
        number_of_urls = len(urls)
        while (i + 1) < number_of_urls:
            url_pairs.append((urls[i], urls[i + 1], i, i + 1))
            i += 1

        i = 0
        current_transaction = []
        end_transactions = False
        all_transactions = []
        timestamp = time[0]
        number_of_pais = len(url_pairs)

        while i < number_of_pais:
            current_url, next_url, index_current, index_next = url_pairs[i]

            # Initialize the transaction for the first URL
            if current_url == '':
                current_transaction.append(next_url)
                timestamp = time[index_next]
                i += 1
                continue

            # If the URL exists in the transaction, end transaction and add it to list
            # If not, we add the url to the transaction list and go on
            if next_url in current_transaction:
                if not end_transactions:
                    if current_transaction not in all_transactions:
                        keywords = MFAlgorithm.keywords_value(dict_urls_keywords, current_transaction)
                        all_transactions.append((visitor, timestamp, current_transaction, keywords))
                this_index = current_transaction.index(next_url)
                current_transaction = current_transaction[0:this_index + 1]
                end_transactions = True
                i += 1
                continue

            else:
                if end_transactions:
                    end_transactions = False
                    timestamp = time[index_current]
                current_transaction.append(next_url)

            i += 1

        if current_transaction not in all_transactions:
            keywords = MFAlgorithm.keywords_value(dict_urls_keywords, current_transaction)
            all_transactions.append((visitor, timestamp, current_transaction, keywords))

        return all_transactions

    @staticmethod
    def init_algorithm(sortedData):
        """

        :param sortedData:
        :return:
        """
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
