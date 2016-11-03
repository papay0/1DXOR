from bs4 import BeautifulSoup
import os
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
import config

def parser(file_content_raw):
    soup = BeautifulSoup(file_content_raw, config.TYPE_PARSER)
    [[s.extract() for s in soup(balise)] for balise in config.TAG_NOT_ALLOWED]
    text = soup.get_text()
    tokenizer = RegexpTokenizer(r'\w+')
    stop = stopwords.words(config.LANG)
    words = [i for i in tokenizer.tokenize(text) if i not in stop]
    print(list(set(words)))

def indexer():
    directory = config.DIRECTORY
    for file in os.listdir(directory):
        if file.endswith(config.EXTENSION):
            f = open(directory+file, 'r')
            parser(f.read())

if __name__ == '__main__':
    indexer()