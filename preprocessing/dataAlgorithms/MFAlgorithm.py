from __future__ import print_function

class MFAlgorithm:

    @staticmethod
    def run_MF_algorithm(visitor, time, path):
        tuples = [('', path[0], 0, 0)]
        i = 0
        length = len(path)
        while (i + 1) < length:
            tuples.append((path[i], path[i + 1], i, i + 1))
            i += 1

        i = 0
        string = []
        flag = 1
        result = []
        timestamp = time[0]
        length_tuples = len(tuples)

        while i < length_tuples:
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
        visitors = sortedData.visitorId.unique()
        paths = []
        i = 0
        visitor_length = len(visitors)
        print("Initializing Data Extraction...")
        for visitor in visitors:
            dataResult = sortedData.loc[sortedData['visitorId'] == visitor]
            path = dataResult.pageUrl.tolist()
            timestamps = dataResult.timestamp.get_values()
            paths.append((visitor, timestamps, path))
            sortedData = sortedData.iloc[len(dataResult):]
            i += 1
            print("Progress:", round((i/visitor_length)*100, 2), "%")
        result = []

        print("Initializing Algorithm...")
        for elem in paths:
            visitor, time, path = elem
            resultPaths = MFAlgorithm.run_MF_algorithm(visitor, time, path)
            result.extend(resultPaths)
        return result

