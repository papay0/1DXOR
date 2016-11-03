import os
import config

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def insert(document_name, words, database):
    for word in words:
        if word in database and document_name not in database[word]:
            database[word].append(document_name)
        else:
            database[word] = [document_name]
    print(document_name)
    print(words)
    print(" ")


def parser(file_content_raw):
    soup = BeautifulSoup(file_content_raw, config.TYPE_PARSER)
    [[s.extract() for s in soup(balise)] for balise in config.TAG_NOT_ALLOWED]
    text = soup.get_text()
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words(config.LANG)
    words = [i for i in tokenizer.tokenize(text) if i not in stop]
    return words

def indexer(database, stemmer):
    directory = config.DIRECTORY
    for file in os.listdir(directory):
        if file.endswith(config.EXTENSION):
            f = open(directory+file, 'r')
            words = [stemmer.stem(word) for word in parser(f.read())]
            insert(os.path.basename(f.name), words, database)

if __name__ == '__main__':
    dict = {}

    client = config.CLIENT
    stemmer = config.STEMMER
    db = client.dict_database
    db_docs = db.docs

    indexer(dict, stemmer)
    db.docs.insert(dict)