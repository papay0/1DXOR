#!/usr/bin/python3

""" This module provides functions to augment a query """

import sys

from SPARQLWrapper import SPARQLWrapper, JSON
from query_helpers import to_query

SPARQL_CLIENT = SPARQLWrapper("http://localhost:3030/Filmographie_instances_saturee/sparql")

def augment(query):
    """ augment a given query """

    def find_all_linked_instances(query):
        """
        find all words which can be infered using matches on
        the query and on semantic triples
        """

        instances = set()
        query_lst = list(query)
        for word_id, word1 in enumerate(query_lst):
            for word2 in list(query)[word_id+1:]:
                instances |= find_linked_instances(word1, word2)
        return instances

    def find_linked_instances(word1, word2):
        """ find all words which associates the two given words in semantic triples """

        linked = set()
        SPARQL_CLIENT.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE {
              ?o1 rdfs:label ?labelTemp1.
              FILTER (regex(?labelTemp1, "^"""+word1+"""$") && (regex(lang(?labelTemp1), 'fr|^$')))
              ?o2 rdfs:label ?labelTemp2.
              FILTER (regex(?labelTemp2, "^"""+word2+"""$") && (regex(lang(?labelTemp2), 'fr|^$')))
              FILTER(?o1 != ?o2).
              {?o1 ?o2 ?res}
               UNION {?o1 ?res ?o2}
               UNION {?res ?o1 ?o2}
               UNION {?o2 ?o1 ?res}
               UNION {?o2 ?res ?o1}
               UNION {?res ?o2 ?o1}.
              ?res rdfs:label ?label.
              FILTER (regex(lang(?label), 'fr|^$'))
            } 
            """)

        SPARQL_CLIENT.setReturnFormat(JSON)
        results = SPARQL_CLIENT.query().convert()

        for result in results["results"]["bindings"]:
            linked.add(result["label"]["value"])

        return linked

    def find_synonyms(word):
        """ find synonyms of the given words according to its semantic """

        synonyms = set()
        SPARQL_CLIENT.setQuery("""
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?label
            WHERE {
              ?subject rdfs:label ?labelTemp.
              FILTER (regex(?labelTemp, "^"""+word+"""$") && (regex(lang(?labelTemp), 'fr|^$')))
              ?subject rdfs:label ?label.
              FILTER (regex(lang(?label), 'fr|^$'))
            } 
            """)

        SPARQL_CLIENT.setReturnFormat(JSON)
        results = SPARQL_CLIENT.query().convert()

        if len(results["results"]["bindings"]) < 1:
            synonyms.add(word)

        for result in results["results"]["bindings"]:
            synonyms.add(result["label"]["value"])

        return synonyms

    new_query = set()
    new_query |= find_all_linked_instances(query)

    for word in query:
        synonyms = find_synonyms(word)
        new_query |= synonyms

    return new_query


if __name__ == "__main__":
    print(augment(to_query(sys.argv)))
