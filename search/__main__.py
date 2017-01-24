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

def select(choices, default, message):
    """ Make a choice from a selection """
    res = None
    while res not in choices:
        print(message +" ["+ "/".join([str(w)+("*" if w == default else "") for w in choices])+"]")
        res = input()
        if res == "":
            return default
    return res


def main(query):
    """ Make a search using program input as base query """
    search_engine = SearchEngine(augment, stem_query, "localhost:27017")
    search_engine.search(query)
    results = search_engine.get_results()
    tfs = ["simple", "normalized", "robertson"]
    dists = ["scalar", "dice", "cosinus", "jaccard"]


    tf = select(tfs, "normalized", "TF method")
    dist = select(dists, "scalar", "Distance method")
    idf = select(["Y", "N"], "Y", "Use idf") == "Y"

    print(results.get_scores(tf, dist, idf))


if __name__ == "__main__":
    main(argv_to_query(sys.argv))
