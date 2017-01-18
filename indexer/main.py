import os
import config
import time
import pprint

from html5lib import HTMLParser
from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from collections import Counter
from htmlfileindexer import HTMLFileIndexer

class HTMLBundleIndexer:
    def __init__(self, fileindexer):
        self.fileindexer = fileindexer

    def run(self, directory):
        indexByDocuments = []

        for file in [ f for f in os.listdir(directory) if f.endswith("html")]:
            try:
                wordsCount = self.fileindexer.run(directory+file)
            except UnicodeDecodeError:
                print(file+"'s encoding is not UTF8")
            else:
                indexByDocuments.append({"name": file, "words": wordsCount})

        indexByWords = self.generateIndexByDocumentsFromIndexByWords(indexByDocuments)

        return (indexByDocuments, indexByWords)

    def generateIndexByDocumentsFromIndexByWords(self, indexByDocuments):
        indexByWords = []
        wordPosition = 0
        referencedWords = {}
        for document in indexByDocuments:
            for word in document["words"]:
                if word not in referencedWords:
                    indexByWords.append({"word": word, "documents": [{"name": document["name"], "count": document["words"][word]}]})
                    referencedWords[word] = wordPosition
                    wordPosition = wordPosition + 1
                else:
                    indexByWords[referencedWords[word]]["documents"].append({"name": document["name"], "count": document["words"][word]})

        return indexByWords

def cleanDB(db):
    db.words.drop()
    db.documents.drop()

if __name__ == '__main__':
    db = config.DB
    cleanDB(db)
    db.run
    indexer = HTMLBundleIndexer(HTMLFileIndexer(config))
    documents, words = indexer.run(config.DIRECTORY)
    # db.documents.ensure_index('documents', unique=True)
    db.documents.insert(documents)
    db.words.insert(words)
    
    print("Indexing Done !")
