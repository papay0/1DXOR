#!/usr/bin/python3

"""
This module contains the SearchEngine class.
"""

import collections
from pymongo import MongoClient
import numpy as np

IndexDatabase = collections.namedtuple("IndexDatabase", ["words", "documents"])

class MatchingDocuments(object):
    """ Associate a document name with an id """

    def __init__(self):
        self.documents_ids = {}
        self.documents = []

    def add_document(self, document_name):
        """add a document """
        if self.documents_ids.get(document_name) is None:
            self.documents_ids[document_name] = len(self.documents)
            self.documents.append(document_name)

    def get_name(self, index):
        """get a document form an id"""
        return self.documents[index]

    def get_index(self, name):
        """get a document index from its name """
        return self.documents_ids[name]

    def size(self):
        return len(self.documents)

class SearchEngine(object):
    """ class used to search in document database """

    def __init__(self, augment, stem, mongo_url):
        self.augment = augment
        self.stem = stem
        self._mongo_client = MongoClient(mongo_url).index_database
        documents = self._mongo_client.documents
        words = self._mongo_client.words
        self.index_db = IndexDatabase(words, documents)

    def search(self, query):
        """ Make a query """
        query = self.augment(query)
        query = self.stem(query)
        self.query(query)

    def query(self, query):
        """ Implement the logic of searching """
        matching_couples = [self.find_documents_for_word(word) for word in query]
        matching_documents = self._create_matching_documents(matching_couples)
        matrix = self._build_matrix(matching_couples, matching_documents)
        print(matrix)


    def find_documents_for_word(self, word):
        """ Get the documents containing word "word" """
        results = self.index_db.words.find({"word":word})
        if results.count() > 0:
            return results[0]["documents"]
        else:
            return []

    def _document_count(self):
        count = self.index_db.documents.count()
        print(count)

    def _create_matching_documents(self, results):
        matching_documents = MatchingDocuments()

        for word_results in results:
            for document in word_results:
                matching_documents.add_document(document["name"])
        print(matching_documents.documents)
        return matching_documents

    def _build_matrix(self, results, matching_documents):
        """ build a match matrix """
        matrix = np.zeros([matching_documents.size(), len(results)])

        for word_id, word_result in enumerate(results):
            for doc_result in word_result:
                doc_index = matching_documents.get_index(doc_result["name"])
                matrix[doc_index, word_id] = doc_result["count"]
        return matrix
