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
        vector = TfidVectorizer(tokenizer=CalculateSimilarity.tokens)
        tfidf = vector.fit_transform(used_items+not_used_items)
        used_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[:used_items_length]]
        not_used_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[used_items_length:]]
        paired_items = []
        similarities_result = []

        for r in itertools.product(used_items_vectors, not_used_items_vectors):
            paired_items.extend([(r[0], r[1])])

        for item1, item2 in paired_items:
            similarity = cosine_similarity(item1, item2)
            similarities_result.extend([(similarity.item(0, 0), item1, item2)])

        return similarities_result.sort()
