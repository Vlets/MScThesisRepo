import pandas as pd
from pandas.io.json import json_normalize


class NormalizePersona:

    @staticmethod
    def normalize_table_personas(sorted_data):
        global_persona_id_scores = [pd.DataFrame(json_normalize(x)) for x in [[y[0]] if len(y) > 1 else y for y
                                                                              in sorted_data['globalPersonaIdScores']]]
        global_persona_id_scores = [pd.DataFrame(data={'id': ["None"], 'score': [0.0]}) if elem.empty else elem for elem
                                    in global_persona_id_scores]
        global_persona_id_scores = pd.concat(global_persona_id_scores)
        global_persona_id_scores.columns = ['globalPersonaIdScores_id', 'globalPersonaIdScores_score']
        global_persona_id_scores = global_persona_id_scores.reset_index(drop=True)
        global_persona_id_scores['globalPersonaIdScores_score'] = global_persona_id_scores[
            'globalPersonaIdScores_score'].div(100)
        persona_id_scores = [pd.DataFrame(json_normalize(x)) for x in [[y[0]] if len(y) > 1 else y for y
                                                                       in sorted_data['personaIdScores']]]
        persona_id_scores = [pd.DataFrame(data={'id': ["None"], 'score': [0.0]}) if elem.empty else elem for elem
                             in persona_id_scores]
        persona_id_scores = pd.concat(persona_id_scores)
        persona_id_scores.columns = ['personaIdScores_id', 'personaIdScores_score']
        persona_id_scores = persona_id_scores.reset_index(drop=True)
        persona_id_scores['personaIdScores_score'] = persona_id_scores['personaIdScores_score'].div(100)
        sorted_data = sorted_data.drop(columns=['globalPersonaIdScores', 'personaIdScores'])

        return pd.concat([sorted_data, global_persona_id_scores, persona_id_scores], axis=1)
