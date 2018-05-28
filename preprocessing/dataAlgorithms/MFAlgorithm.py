class MFAlgorithm:

    @staticmethod
    def run_MF_algorithm(visitor, time, path):
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
                        result.append((visitor, timestamp, string))
                string.append(varB)
                timestamp = time[indexB]
                i += 1
                continue

            if varB in string:
                if flag == 1:
                    if string not in result:
                        result.append((visitor, timestamp, string))
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
            result.append((visitor, timestamp, string))

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
            result_paths = MFAlgorithm.run_MF_algorithm(visitorId, time, path)
            result.extend(result_paths)
            i += 1
            if i % 100 == 0:
                print("Progress:", round((i / visitor_length) * 100, 2), "%")
        return result