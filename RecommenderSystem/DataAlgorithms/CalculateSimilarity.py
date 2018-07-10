from sklearn.feature_extraction.text import TfidfVectorizer as TfidVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import itertools


class CalculateSimilarity:

    @staticmethod
    def tokens(s):
        return s.split(' ')

    @staticmethod
    def similarity_results(seen_items, not_seen_items):
        """
        This method calculates the similarity between seen items and not
        seen items based of their keywords.
        :param seen_items: List of tuples with the URL of seen items and
        their associated keywords
        :param not_seen_items: List of tuples with the URL of not seen items
        and their associated keywords
        :return: A list of tuples with their score of similarity, the URL of the
        seen item and the URL of the not seen item
        """
        seen_items_length = len(seen_items)
        # used_items_keywords = [y for x, y in used_items]
        not_seen_items_keywords = [y for x, y in not_seen_items]
        vectorizer = TfidVectorizer(tokenizer=CalculateSimilarity.tokens)
        tfidf = vectorizer.fit_transform(seen_items + not_seen_items_keywords)
        seen_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[:seen_items_length]]
        seen_items_vectors = list(zip(seen_items_vectors, seen_items))
        not_seen_items_vectors = [x.reshape(1, -1) for x in tfidf.toarray()[seen_items_length:]]
        not_seen_items_vectors = list(zip(not_seen_items_vectors, not_seen_items))
        paired_seen_unseen_items = []
        similarities_result = []

        for r in itertools.product(seen_items_vectors, not_seen_items_vectors):
            paired_seen_unseen_items.extend([(r[0], r[1])])

        for key, value in paired_seen_unseen_items:
            keywords1, des1 = key
            # name1, des1 = pair1
            keywords2, pair2 = value
            name2, des2 = pair2
            similarity = cosine_similarity(keywords1, keywords2)
            similarities_result.extend([(similarity.item(0, 0), name2)])

        return similarities_result
