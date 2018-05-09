class MFAlgorithm:

    @staticmethod
    def run_MF_algorithm(path):
        tuples = [('', path[0])]
        i = 0
        while (i + 1) < len(path):
            tuples.append((path[i], path[i + 1]))
            i += 1

        i = 0
        string = []
        flag = 1
        result = []

        while i < len(tuples):
            varA, varB = tuples[i]

            if varA == '':
                if string != []:
                    if string not in result:
                        result.append(string)
                string.append(varB)
                i += 1
                continue

            if varB in string:
                if flag == 1:
                    if string not in result:
                        result.append(string)
                index = string.index(varB)
                string = string[0:index + 1]
                flag = 0
                i += 1
                continue

            else:
                string.append(varB)
                if flag == 0:
                    flag = 1

            i += 1

        if string not in result:
            result.append(string)

        return result

    @staticmethod
    def init_algorithm(sortedData):
        visitors = sortedData.visitorId.unique()
        paths = []

        for visitor in visitors:
            path = []
            dataResult = sortedData.loc[sortedData['visitorId'] == visitor]
            urls = dataResult.pageUrl
            for url in urls:
                path.append(url)
            paths.append((visitor, path))

        result = []

        for elem in paths:
            visitor, path = elem
            resultPaths = MFAlgorithm.run_MF_algorithm(path)
            result.append((visitor, resultPaths))
        return result
