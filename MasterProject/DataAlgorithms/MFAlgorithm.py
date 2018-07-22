
class MFAlgorithm:


    @staticmethod
    def run_MF_algorithm(visitor, time, urls):
        """

        :param urls:
        :param visitor:
        :param time:
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
        number_of_pairs = len(url_pairs)

        while i < number_of_pairs:
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
                        all_transactions.append((visitor, timestamp, current_transaction))
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
            all_transactions.append((visitor, timestamp, current_transaction))

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
            result_paths = MFAlgorithm.run_MF_algorithm(visitorId, time, path)
            result.extend(result_paths)
            i += 1
            if i % 100 == 0:
                print("Progress:", round((i / visitor_length) * 100, 2), "%")
        return result
