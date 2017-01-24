from pymongo import MongoClient
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer

LANG = 'french'
DIRECTORY = './corpus/'
EXTENSION = 'html'
TAG_NOT_ALLOWED = ['script', 'style']
TYPE_PARSER = 'html.parser'
STEMMER = SnowballStemmer('french')
STOPWORDS = stopwords.words(LANG)
TOKENIZER = RegexpTokenizer(r'\w+')
DB = MongoClient('localhost', 27017).index_database
