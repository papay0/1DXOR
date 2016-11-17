import os
import config
import time

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter

# build the dictionnary with this schema {'word1': ['doc1', 'doc2', 'word2': ['doc4', 'doc7']]}
def build_dict_words(document_name, words, database):
    for word in words:
        if word not in database:
            database[word] = [{document_name:1}]
        else:
            found = False
            for document_obj in database[word]:
                if document_name in document_obj:
                    document_obj[document_name] += 1
                    found = True
            if not found:
                database[word].append({document_name: 1})

# parse the content of the website - return the words filtered (without the stopwords, stemmer)
def parser(file_content_raw, stemmer):
    soup = BeautifulSoup(file_content_raw, config.TYPE_PARSER)
    [[s.extract() for s in soup(balise)] for balise in config.TAG_NOT_ALLOWED]
    text = soup.get_text()
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words(config.LANG)
    words = [stemmer.stem(word) for word in tokenizer.tokenize(text)]
    words = [i.lower() for i in words if i.lower() not in stop]
    return words

# for each file, insert into DB of documents, build dictionnary of words
def indexer(database_words, stemmer):
    directory = config.DIRECTORY
    for file in os.listdir(directory):
        if file.endswith(config.EXTENSION):
            f = open(directory+file, 'r')
            name_document = os.path.basename(f.name).split('.')[:-1][0] # Have only the name without the extension
            words = parser(f.read(), stemmer)
            insert_db_documents(name_document, dict(Counter(words))) # db.documents: {_id: D1, words: ['coucou': 2, 'salut": 3, ...]}
            build_dict_words(name_document, words, database_words) # database_words: {'word': [D1, D2, Dn...]}

# insert into DB of documents: {'_id': D1, 'words': {word1: 2, word2: 7, ...}})
def insert_db_documents(name_document, words_with_occurence):
    db.documents.insert({'_id': name_document, 'words': words_with_occurence})

# insert into DB of words: {_id: word1, documents: [D1, D4, D7]}
def insert_db_words(database_words):
    for word in database_words:
        db.words.insert({'_id': word, 'documents': database_words[word]})

def cleanDB():
    db.words.drop()
    db.documents.drop()

def solver():
    database_words = {}
    cleanDB()

    indexer(database_words, config.STEMMER)
    insert_db_words(database_words)

    db.words.insert(database_words)

if __name__ == '__main__':
    global db
    db = config.DB
    start = time.time()
    solver()
    end = time.time()
    print(end-start, "seconds")