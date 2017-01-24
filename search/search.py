#!/usr/bin/python3

"""
This module contains the SearchEngine class.
"""

from pymongo import MongoClient
import numpy as np

class SearchResult(object):
    """ Results of a search """

    def __init__(self, query_vector, doc_vectors, idf, docs_stats):
        self.query = query_vector
        self.doc_vectors = doc_vectors
        self._doc_names = self.doc_vectors.keys()
        self._doc_stats = docs_stats
        self.idf = idf

    def get_scores(self, tf_method="simple", distance_method="scalar", use_idf=False):
        """ get the score of each document """

        def get_distance(method, Q, D):
            """ compute distance between query vector and document vector """
            QD = Q@D
            if method is "scalar":
                return QD
            else:
                Q2 = Q@Q
                D2 = D@D
                if method is "dice":
                    return 2*QD/(Q2+D2)
                elif method is "cosinus":
                    return QD/np.sqrt(Q2+D2)
                elif method is "jaccard":
                    return QD/(Q2+D2-QD)
                else:
                    raise KeyError

        Ds = self._get_tf(tf_method)
        Q = self.query.weights[:]
        if use_idf:
            Ds = Ds*self.idf

        scores = []
        for doc_id, doc_name in enumerate(self._doc_names):
            score = get_distance(distance_method, Q, Ds[doc_id])
            scores.append((doc_name, score))
        return sorted(scores, reverse=True, key=lambda item: item[1])

    def _get_tf(self, method):
        tf = np.empty([len(self._doc_names), self.query.shape[0]])
        for doc_id, doc_name in enumerate(self._doc_names):
            tf[doc_id] = self.doc_vectors[doc_name]

        if method is "simple":
            return tf
        elif method is "normalized":
            for doc_id, doc_name in enumerate(self._doc_names):
                tf[doc_id] = tf[doc_id]/self._doc_stats[doc_name]["max"]
        elif method is "robertson":
            mean = np.mean([self._doc_stats[doc_name]["length"] for doc_name in self._doc_stats])
            for doc_id, doc_name in enumerate(self._doc_names):
                tf[doc_id] /= 0.5 + 1.5*(self._doc_stats[doc_name]["max"]/mean)+tf[doc_id]
        else:
            raise KeyError

        return tf


class SearchEngine(object):
    """ class used to search in document database """

    def __init__(self, augment, stem, mongo_url):
        self.augment = augment
        self.stem = stem
        mongo_client = MongoClient(mongo_url).index_database
        self.index_db = {"words": mongo_client.words, "documents": mongo_client.documents}

        self._results = None
        self._query = None
        self._search_results = None

    def search(self, query):
        """ Make a query """
        query = self.augment(query)
        self._query = self.stem(query)
        self._make_query()

    def _make_query(self):
        """ Implement the logic of searching """
        self._results = [(word, self._find_documents_for_word(word)) for word in self._query.words]
        matrix = self._build_documents_vectors()
        doc_stats = self._doc_stats(matrix.keys())
        self._search_results = SearchResult(self._query, matrix, self._idf(), doc_stats)


    def _find_documents_for_word(self, word):
        """ Get the documents containing word "word" """
        results = self.index_db["words"].find_one({"word":word})
        if results is None:
            return []

        return results["documents"]


    def _build_documents_vectors(self):
        """ build a match matrix """
        documents_vectors = dict()
        doc_index = self.index_db["documents"].find({})
        for doc in doc_index:
            documents_vectors[doc["name"]] = np.zeros([self._query_size()])

        for word_index, (_, matches) in enumerate(self._results):
            for match in matches:
                doc_name = match["name"]
                documents_vectors[doc_name][word_index] = match["count"]
        return documents_vectors

    def _query_size(self):
        return self._query.shape[0]

    def _idf(self):
        """ compute the idf of each query term """
        count = self.index_db["documents"].count()
        return [np.log10(count/max(0.01, len(document[1]))) for document in self._results]

    def _doc_stats(self, doc_list):
        stats = dict()
        for doc_name in doc_list:
            doc_index = self.index_db["documents"].find_one({"name": doc_name})
            counts = [doc_index["words"][word] for word in doc_index["words"]]
            stats[doc_name] = {"length": sum(counts), "max": max(counts)}

        return stats

    def get_results(self):
        """ retrieve results """
        return self._search_results
