class MFAlgorithm:

    @staticmethod
    def run_MF_algorithm(path):
        tuples = [('', path[0])]
        i = 0
        while (i + 1) < len(path):
            tuples.append((path[i], path[i + 1]))
            i += 1

        i = 0
        string = ""
        flag = 1
        result = []

        while i < len(tuples):
            varA, varB = tuples[i]

            if varA == '':
                if string != "":
                    result.append(string)
                string = varB
                i += 1
                continue

            if varB in string:
                if flag == 1:
                    result.append(string)
                index = string.index(varB)
                string = string[0:index + 1]
                flag = 0
                i += 1
                continue

            else:
                string += varB
                if flag == 0:
                    flag = 1

            i += 1

        if string != "":
            result.append(string)

        return result
