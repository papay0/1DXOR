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


def input_to_query(argv):
    """ transform argv into a set of words """
    query = " ".join(argv[1:])
    query = [x.strip() for x in query.split(',')]
    return set(query)

def main(argv):
    """ Make a search using program input as base query """
    search_engine = SearchEngine(augment, stem_query, "localhost:27017")
    search_engine.search(input_to_query(argv))


if __name__ == "__main__":
    main(sys.argv)
