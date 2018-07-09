from sklearn.feature_extraction.text import TfidfVectorizer as TfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools


class CalculateSimilarity:

    @staticmethod
    def tokens(s):
        return s.split(' ')

    @staticmethod
    def similarity_results(used_items, not_used_items):
        """
        This method calculates the similarity between seen items and not
        seen items based of their keywords.
        :param used_items: List of tuples with the URL of seen items and
        their associated keywords
        :param not_used_items: List of tuples with the URL of not seen items
        and their associated keywords
        :return: A list of tuples with their score of similarity, the URL of the
        seen item and the URL of the not seen item
        """
        used_items_length = len(used_items)
        # used_items_keywords = [y for x, y in used_items]
        not_used_items_keywords = [y for x, y in not_used_items]
        vectorizer = TfidVectorizer(tokenizer=CalculateSimilarity.tokens)
        tfidf = vectorizer.fit_transform(used_items + not_used_items_keywords)
        used_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[:used_items_length]]
        used_items_vectors = list(zip(used_items_vectors, used_items))
        not_used_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[used_items_length:]]
        not_used_items_vectors = list(zip(not_used_items_vectors, not_used_items))
        paired_items = []
        similarities_result = []

        for r in itertools.product(used_items_vectors, not_used_items_vectors):
            paired_items.extend([(r[0], r[1])])

        for key, value in paired_items:
            keywords1, des1 = key
            # name1, des1 = pair1
            keywords2, pair2 = value
            name2, des2 = pair2
            similarity = cosine_similarity(keywords1, keywords2)
            similarities_result.extend([(similarity.item(0, 0), name2)])

        return similarities_result
