"""
this module contains a method to stem queries
"""

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer
import numpy


def stem_query(query):
    """ stem each string of a query"""
    stemmer = SnowballStemmer('french')
    stop = stopwords.words('french')

    def stem_word(word):
        """ stem a word """
        return stemmer.stem(word)

    tokenizer = RegexpTokenizer('\\w+')
    new_query = []
    added_words = set()
    for term, weight in query:
        subterms = tokenizer.tokenize(term.lower())
        subterms = [stem_word(subterm) for subterm in subterms if subterm not in stop]
        for subterm in subterms:
            if subterm not in added_words:
                new_query.append((subterm, float(weight)))
                added_words.add(subterm)

    return numpy.rec.array(new_query, dtype=[('words', object), ('weights', 'f4')])
