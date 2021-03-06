import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities
from collections import defaultdict

import pymongo
connection = pymongo.MongoClient("mongodb://localhost")
db = connection.thesis
nyt = db.nyt


cursor = db.nyt.find()
documents = []


# adding all keywords
for document in cursor:
	documents.append((document['keywords']))

print(documents)

# determining and removing keywords that appear only once
freq = defaultdict(int)
allwords = []
for words in documents:
	for word in words:
		allwords.append(word)
		freq[word] += 1

# print(freq);

keys = [[token for token in text if freq[token] > 1]
	for text in documents]

# print(keys)

# vectorizing keywords and frequency
dictionary = corpora.Dictionary(keys)
corpus = [dictionary.doc2bow(text) for text in keys]
# print(corpus)

# transforming the corpus
# initualizing a model
tfidf = models.TfidfModel(corpus)
# print(tfidf)
