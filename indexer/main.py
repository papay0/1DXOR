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
            print(document)
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
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(results)

#class Indexer:
#    wordsIndex = {}
#    documentsIndex = {}
#
#    def __init__(self, config):
#        self.stemmer = config.STEMMER
#        self.stopWords = stopwords.words(config.LANG)
#        self.tags_not_allowed = config.TAG_NOT_ALLOWED
#        self.type_parser = config.TYPE_PARSER
#
#        self.tokenizer = RegexpTokenizer(r'\w+')
#
#    # build the dictionnary with this schema {'word1': ['doc1', 'doc2'], 'word2': ['doc4', 'doc7']}
#    def build_dict_words(self, document_name, words, database):
#        for word in words:
#            if word not in database:
#                database[word] = [{document_name:1}]
#            else:
#                found = False
#                for document_obj in database[word]:
#                    if document_name in document_obj:
#                        document_obj[document_name] += 1
#                        found = True
#                if not found:
#                    database[word].append({document_name: 1})
#
#    # parse the content of the website - return the words filtered (without the stopwords, stemmer)
#    def parseFileContent(self, file_content):
#        try:
#            soup = BeautifulSoup(file_content, self.type_parser)
#        except HTMLParser.HTMLParseError:
#            print("Oups, UTF8?, file: ", f.name)
#        else:
#            [[s.extract() for s in soup(balise)] for balise in self.tags_not_allowed]
#            text = soup.get_text()
#            stems = self.extractStems(text)
#        return stems
#
#    def extractStems(self, text):
#        stems = [self.stemmer.stem(word) for word in self.tokenize(text)]
#        filteredStems = [i.lower() for i in stems if i.lower() not in stop and i != "_id"]
#        return filteredStems
#
#    def tokenize(self, text):
#        return self.tokenizer.tokenize(text)
#
#
#    # for each file, insert into DB of documents, build dictionnary of words
#    def run(self):
#        directory = config.DIRECTORY
#        for file in os.listdir(directory):
#            if file.endswith(config.EXTENSION):
#                f = open(directory+file, 'r')
#                name_document = os.path.basename(f.name).split('.')[:-1][0] # Have only the name without the extension
#                words = self.parseFileContent(f.read())
#                self.insert_db_documents(name_document, dict(Counter(words))) # db.documents: {_id: D1, words: ['coucou': 2, 'salut": 3, ...]}
#                self.build_dict_words(name_document, words) # database_words: {'word': [D1, D2, Dn...]}
#
#    # insert into DB of documents: {'_id': D1, 'words': {word1: 2, word2: 7, ...}})
#    def insert_db_documents(self, name_document, words_with_occurence):
#        # print("name document: ", name_document)
#        db.documents.insert({'_id': name_document, 'words': words_with_occurence})
#
#    def run(self):
#        database_words = {}
#        
#        self.indexer(database_words)
#        self.insert_db_words(database_words)
#
#        print(database_words)
#        db.words.insert(database_words)

#if __name__ == '__main__':
#    global db
#    start = time.time()
#    indexer = Indexer(config)
#    index = indexer.run()
#
#    # Store results
#    db = config.DB
#    indexDB = IndexDB(db)
#    indexDB.store()
#    end = time.time()
#    print(end-start, "seconds")
