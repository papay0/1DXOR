import os
import config
from bs4 import BeautifulSoup
from collections import Counter
import pprint
import re

class HTMLFileIndexer:

    def __init__(self, config):
        self.stemmer = config.STEMMER
        self.stopWords = config.STOPWORDS
        self.tags_not_allowed = config.TAG_NOT_ALLOWED
        self.type_parser = config.TYPE_PARSER

        self.tokenizer = config.TOKENIZER

    def run(self, file):
        f = open(file, 'r')
        html = f.read()
        text = self.textify(html)
        words = self.stemAndCount(text)
        return words

    # Remove tags from an text/html document
    def textify(self, html):
        try:
            soup = BeautifulSoup(html, "html.parser")
        except:
            print("Oups, UTF8?")
            return ""
        else:
            [[s.extract() for s in soup(balise)] for balise in self.tags_not_allowed]
            text = soup.get_text()
            return self.removeURLs(text)

    def removeURLs(self, text):
        return re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)


    def stemAndCount(self, text):
        words = self.tokenizer.tokenize(text)
        stems = [self.stemmer.stem(word).lower() for word in words]
        filteredStems = [stem for stem in stems if stem not in self.stopWords and stem[0] != "_"]
        return dict(Counter(filteredStems))

    def tokenize(self, text):
        return self.tokenizer.tokenize(text)

if __name__ == '__main__':
    indexer = HTMLFileIndexer(config)
    testFile = open(os.path.dirname(os.path.abspath(__file__))+"/test.html")
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(indexer.run(testFile))
