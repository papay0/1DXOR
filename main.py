import os
import config

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

def insert(document_name, words, database):
    for word in words:
        if word in database:
            database[word].append(document_name)
        else:
            database[word] = [document_name]
    print(document_name)
    print(words)
    print(database)
    print(" ")


def parser(file_content_raw):
    soup = BeautifulSoup(file_content_raw, config.TYPE_PARSER)
    [[s.extract() for s in soup(balise)] for balise in config.TAG_NOT_ALLOWED]
    text = soup.get_text()
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words(config.LANG)
    words = [i for i in tokenizer.tokenize(text) if i not in stop]
    #print(list(set(words)), end="\n\n")
    return words

def indexer(database):
    directory = config.DIRECTORY
    for file in os.listdir(directory):
        if file.endswith(config.EXTENSION):
            f = open(directory+file, 'r')
            words = parser(f.read())
            insert(os.path.basename(f.name), words, database)

if __name__ == '__main__':
    db = {}
    indexer(db)