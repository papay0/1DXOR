"""
this module contains a method to stem queries
"""

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer


def stem_query(query):
    """ stem each string of a query"""
    stemmer = SnowballStemmer('french')
    stop = stopwords.words('french')

    def stem_word(word):
        """ stem a word """
        return stemmer.stem(word)

    query_str = ' '.join(list(query))
    tokenizer = RegexpTokenizer(r'\w+')
    terms = tokenizer.tokenize(query_str)

    terms = [stem_word(term) for term in terms]
    terms = [i.lower() for i in terms if i.lower() not in stop]
    return set(terms)

