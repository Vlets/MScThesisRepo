from sklearn.feature_extraction.text import TfidfVectorizer as TfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools

class CalculateSimilarity:

    @staticmethod
    def tokens(s):
       return s.split(' ')

    @staticmethod
    def similarity_results(used_items, not_used_items):
        used_items_length = len(used_items)
        used_items_categories = [y for x, y in used_items]
        not_used_items_categories = [y for x, y in not_used_items]
        vector = TfidVectorizer(tokenizer=CalculateSimilarity.tokens)
        tfidf = vector.fit_transform(used_items_categories+not_used_items_categories)
        used_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[:used_items_length]]
        used_items_vectors = list(zip(used_items_vectors, used_items))
        not_used_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[used_items_length:]]
        not_used_items_vectors = list(zip(not_used_items_vectors, not_used_items))
        paired_items = []
        similarities_result = []

        for r in itertools.product(used_items_vectors, not_used_items_vectors):
            paired_items.extend([(r[0], r[1])])

        for key, value in paired_items:
            categories1, pair1 = key
            name1, des1 = pair1
            categories2, pair2 = value
            name2, des2 = pair2
            similarity = cosine_similarity(categories1, categories2)
            similarities_result.extend([(similarity.item(0, 0), name1, name2)])

        return similarities_result
