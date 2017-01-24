#!/usr/bin/python3

""" This module provides functions to augment a query """

import sys

from SPARQLWrapper import SPARQLWrapper, JSON
import numpy
from query_helpers import argv_to_query

SPARQL_CLIENT = SPARQLWrapper("http://localhost:3030/Filmographie_instances_saturee/sparql")

def augment(query):
    """ augment a given query """

    def find_all_linked_instances(query):
        """
        find all words which can be infered using matches on
        the query and on semantic triples
        """

        instances = set()
        query_lst = query
        for word_id, word1 in enumerate(query_lst):
            for word2 in list(query)[word_id+1:]:
                w1 = " .*".join(word1.split())
                w2 = " .*".join(word2.split())
                print(w1)
                print(w2)
                instances |= find_linked_instances(w1, w2)
                a = find_linked_third_strategy(w1, w2)
                print(a)
                instances |= a
        return instances

    def find_linked_third_strategy(word1, word2):
        """ find all words which are of type word1 """
        linked = set()
        SPARQL_CLIENT.setQuery(
	    """PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
	    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
	    SELECT ?label
	    WHERE {
	      ?typeOrLink1 rdfs:label $label1.
	      ?typeOrLink2 rdfs:label $label2.
	      FILTER(regex(?label1, "^"""+word1+"""$") && regex(lang(?label1),"^$|fr")).
	      FILTER(regex(?label2, "^"""+word2+"""$") && regex(lang(?label2),"^$|fr")).
	      {
		?object rdf:type $typeOrLink1.
		?object ?pred ?typeOrLink2
	      } UNION
	      {
		?object rdf:type $typeOrLink2.
		?object ?pred ?typeOrLink1
	      }.
	      ?object rdfs:label ?label
	    }
	    """)

        SPARQL_CLIENT.setReturnFormat(JSON)
        results = SPARQL_CLIENT.query().convert()
        for result in results["results"]["bindings"]:
            linked.add(result["label"]["value"])

        return linked

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

    linked = find_all_linked_instances(query)
    synonyms = set()
    for word in query:
        synonyms |= find_synonyms(word)

    new_query = []
    added_words = set()

    for word in query:
        if word not in added_words:
            new_query.append((word, 1))
            added_words.add(word)
 
    for word in synonyms:
        if word not in added_words:
            new_query.append((word, 0.2))
            added_words.add(word)

    for word in linked:
        if word not in added_words:
            new_query.append((word, max(0.5, 0.8/len(linked))))
            added_words.add(word)

    return numpy.rec.array(new_query, dtype=[('words', object), ('weights', 'f4')])


if __name__ == "__main__":
    print(augment(argv_to_query(sys.argv)))
