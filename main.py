import os
import config

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter

def insert(document_name, words, database):
    for word in words:
        if word in database and document_name not in database[word]:
            database[word].append(document_name)
        else:
            database[word] = [document_name]


def parser(file_content_raw, stemmer):
    soup = BeautifulSoup(file_content_raw, config.TYPE_PARSER)
    [[s.extract() for s in soup(balise)] for balise in config.TAG_NOT_ALLOWED]
    text = soup.get_text()
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words(config.LANG)
    words = [stemmer.stem(word) for word in tokenizer.tokenize(text)]
    words = [i.lower() for i in words if i.lower() not in stop]
    #print(words)
    return words

def indexer(database_words, database_documents, stemmer):
    directory = config.DIRECTORY
    for file in os.listdir(directory):
        if file.endswith(config.EXTENSION):
            f = open(directory+file, 'r')
            name_document = os.path.basename(f.name).split('.')[:-1][0] # Have only the name without the extension
            words = parser(f.read(), stemmer)
            database_documents[name_document] = dict(Counter(words))
            insert(name_document, words, database_words)

if __name__ == '__main__':
    dict_key_word = {}
    dict_key_document = {}

    client = config.CLIENT
    stemmer = config.STEMMER
    db = client.index_database
    db_docs = db.key_documents
    db_words = db.key_words

    indexer(dict_key_word, dict_key_document, stemmer)
    print("Ok")
    #print(dict_key_word)
    #print(dict_key_document)
    db.key_documents.insert(dict_key_document)
    db.key_words.insert(dict_key_word)