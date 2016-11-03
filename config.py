from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer

LANG = 'french'
DIRECTORY = './corpus/'
EXTENSION = 'html'
TAG_NOT_ALLOWED = ['script', 'style']
TYPE_PARSER = 'html.parser'
CLIENT= MongoClient('localhost', 27017)
STEMMER = SnowballStemmer('french')