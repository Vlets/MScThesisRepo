import pandas as pd
import numpy as np
from pandas.io.json import json_normalize


class NormalizePersona:

    @staticmethod
    def normalize_table_personas(sortedData):
        sortedDataEdit = sortedData[(sortedData.astype(str)['globalPersonaIdScores'] != '[]') |
                                        (sortedData.astype(str)['personaIdScores'] != '[]')]
        sortedDataEdit = sortedDataEdit.reset_index().drop('index', axis=1)
        globalPersonaIdScores = [pd.DataFrame(json_normalize(x)) for x in sortedDataEdit['globalPersonaIdScores']]
        personaIdScores = [pd.DataFrame(json_normalize(x)) for x in sortedDataEdit['personaIdScores']]
        sortedDataEdit = sortedDataEdit.drop(columns=['globalPersonaIdScores', 'personaIdScores'])
        sortedDataEdit['globalPersonaIdScores.id'] = "None"
        sortedDataEdit['globalPersonaIdScores.score'] = np.nan
        sortedDataEdit['personaIdScores.id'] = "None"
        sortedDataEdit['personaIdScores.score'] = np.nan

        i = 0

        while i < len(sortedDataEdit):
            if len(globalPersonaIdScores[i]) > 1:
                auxGPIS = globalPersonaIdScores[i][:-1]
            else:
                auxGPIS = globalPersonaIdScores[i]

            if len(personaIdScores[i]) > 1:
                auxPIS = personaIdScores[i][:-1]
            else:
                auxPIS = personaIdScores[i]

            if not auxGPIS.empty:
                sortedDataEdit.at[i, 'globalPersonaIdScores.id'] = auxGPIS.at[0, 'id']
                sortedDataEdit.at[i, 'globalPersonaIdScores.score'] = auxGPIS.at[0, 'score']

            if not auxPIS.empty:
                sortedDataEdit.at[i, 'personaIdScores.id'] = auxPIS.at[0, 'id']
                sortedDataEdit.at[i, 'personaIdScores.score'] = auxPIS.at[0, 'score']

            i += 1

        return sortedDataEdit
