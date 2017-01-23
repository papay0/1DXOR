#!/usr/bin/python3
"""
Usage : python3 __main__.py <QUERY>
where QUERY is a comma separated list of keywords.
Example :
    $ python3 __main__.py Omar Sy, Trappes
"""
import sys

from search import SearchEngine
from augment_query import augment
from stem import stem_query
from query_helpers import argv_to_query


def compute_recall(scores, ground_truth):
    """" compute the recall of a search result"""
    relevant_documents = [doc_relevance[0] for doc_relevance in ground_truth if doc_relevance[1]]
    relevant_selected = [score for score in scores if score[0] in relevant_documents]
    return len(relevant_selected)/len(relevant_documents)

def main(query):
    """ Make a search using program input as base query """
    search_engine = SearchEngine(augment, stem_query, "localhost:27017")
    search_engine.search(query)
    results = search_engine.get_results()
    print(results.get_scores("robertson", "scalar", True))


if __name__ == "__main__":
    main(argv_to_query(sys.argv))
