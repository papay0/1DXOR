#!/usr/bin/python3
""" tools to manipulate queries """
import sys

def to_query(argv):
    """ transform argv into a set of words """
    query = " ".join(argv[1:])
    query = [x.strip() for x in query.split(',')]
    return set(query)


if __name__ == "__main__":
    print(to_query(sys.argv))
