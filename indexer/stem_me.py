import sys

from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer('french')
stop = stopwords.words('french')

sentence = ' '.join(sys.argv[1:])
tokenizer = RegexpTokenizer(r'\w+')
words = [stemmer.stem(word) for word in tokenizer.tokenize(sentence)]
words = [i.lower() for i in words if i.lower() not in stop]
print(" ".join(words), end="")
sys.stdout.flush()