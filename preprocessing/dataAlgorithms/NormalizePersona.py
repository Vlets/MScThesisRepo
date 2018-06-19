import pandas as pd
import numpy as np
from pandas.io.json import json_normalize


class NormalizePersona:

    @staticmethod
    def normalize_table_personas(sortedData):

        globalPersonaIdScores = [pd.DataFrame(json_normalize(x)) for x in [[y[0]] if len(y) > 1 else y for y
                                                                           in sortedData['globalPersonaIdScores']]]
        globalPersonaIdScores = [pd.DataFrame(data={'id': ["None"], 'score': [np.nan]}) if elem.empty else elem for elem
                                 in globalPersonaIdScores]
        globalPersonaIdScores = pd.concat(globalPersonaIdScores)
        globalPersonaIdScores.columns = ['globalPersonaIdScores.id', 'globalPersonaIdScores.score']
        globalPersonaIdScores = globalPersonaIdScores.reset_index(drop=True)
        personaIdScores = [pd.DataFrame(json_normalize(x)) for x in [[y[0]] if len(y) > 1 else y for y
                                                                     in sortedData['personaIdScores']]]
        personaIdScores = [pd.DataFrame(data={'id': ["None"], 'score': [np.nan]}) if elem.empty else elem for elem
                           in personaIdScores]
        personaIdScores = pd.concat(personaIdScores)
        personaIdScores.columns = ['personaIdScores.id', 'personaIdScores.score']
        personaIdScores = personaIdScores.reset_index(drop=True)
        sortedData = sortedData.drop(columns=['globalPersonaIdScores', 'personaIdScores'])

        return pd.concat([sortedData, globalPersonaIdScores, personaIdScores], axis=1)

