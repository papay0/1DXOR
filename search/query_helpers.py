#!/usr/bin/python3
""" tools to manipulate queries """
import sys

def argv_to_query(argv):
    """ transform argv into a set of words """
    query_string = " ".join(argv[1:])
    query = text_to_query(query_string)
    return query

def text_to_query(query_string):
    """ transform argv into a set of words """
    query = [x.strip() for x in query_string.split(',')]
    return set(query)

if __name__ == "__main__":
    print(argv_to_query(sys.argv))
