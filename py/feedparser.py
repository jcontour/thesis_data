from bs4 import BeautifulSoup
from alchemyapi import AlchemyAPI
import pymongo
import feedparser
import nltk
from nltk.corpus import stopwords

alchemyapi = AlchemyAPI() 

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.thesis
rss = db.rss

feeds = [ {'source': 'New York Times', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'}, {'source': 'The New Yorker', 'url': 'http://www.newyorker.com/feed/everything'}, {'source': 'The New Yorker', 'url': 'http://www.newyorker.com/feed/news'}, {'source': 'The New Yorker', 'url': 'http://www.newyorker.com/feed/tech'}, {'source': 'The Atlantic', 'url': 'http://feeds.feedburner.com/TheAtlantic'}, {'source': 'NPR', 'url': 'http://www.npr.org/rss/rss.php?id=1001'}, {'source': 'Time', 'url': 'http://feeds2.feedburner.com/time/topstories'}, {'source': 'Wired', 'url': 'http://feeds.wired.com/wired/index'}, {'source': 'Mother Jones', 'url': 'http://feeds.feedburner.com/motherjones/BlogsAndArticles'}, {'source': 'Vox', 'url': 'http://www.vox.com/rss/index.xml'}, {'source': 'Wall Street Journal', 'url': 'http://www.wsj.com/xml/rss/3_7085.xml'}, {'source': 'Wall Street Journal', 'url': 'http://www.wsj.com/xml/rss/3_7455.xml'}, {'source': 'Slate', 'url': 'http://feeds.slate.com/slate'}, {'source': 'CNN', 'url': 'http://rss.cnn.com/rss/cnn_topstories.rss'}, {'source': 'Forbes', 'url': 'http://www.forbes.com/most-popular/feed/'}, {'source': 'BBC', 'url': 'http://feeds.bbci.co.uk/news/rss.xml'}, {'source': 'The Huffington Post', 'url': 'http://feeds.huffingtonpost.com/c/35496/f/677497/index.rss'}, {'source': 'NBC', 'url': 'http://feeds.nbcnews.com/feeds/topstories'} ]

for source in feeds:
	feed = feedparser.parse(source['url'])

	i = 0
	while i < len(feed.entries):

		# REMOVING HTML FROM DESCRIPTION STRING
		if '<' in feed.entries[i].description:
			soup = BeautifulSoup(feed.entries[i].description, "lxml")
			desc = soup.get_text()
		else:
			desc = feed.entries[i].description

		#getting keywords
		response = alchemyapi.keywords('text', desc)
		allkeywords = []
		keywords = []
		if response['status'] == 'OK':
			for keyword in response['keywords']:
				if ' ' in keyword['text']:
					splitkey = keyword['text'].split()
					for k in splitkey:
						allkeywords.append(k)
				else:
					allkeywords.append(keyword['text'])
		else:
			print('Error in keyword extraction call: ', response['statusInfo'])

		# getting concepts
		response = alchemyapi.concepts('text', desc)
		if response['status'] == 'OK':
			for concept in response['concepts']:
				if ' ' in concept['text']:
					splitconcept = concept['text'].split()
					for c in splitconcept:
						allkeywords.append(c)
				else:
					allkeywords.append(concept['text'])

		else:
			print('Error in concept tagging call: ', response['statusInfo'])

		# removing all duplicate keywords
		# sets cannot have dupes
		uniquekeywords = list(set(allkeywords))

		# removing stopwords
		# nltk stopwords + list comprehension
		keywords = [w for w in uniquekeywords if not w in stopwords.words('english')]

		print("---------------------------------------")


		if len(keywords) > 0:
			# CREATE ENTRY
			entry = {'source': source['source'], 'title': feed.entries[i].title, 'link': feed.entries[i].link, 'description': desc, 'date': feed.entries[i].published, 'keywords': keywords}
			# INSERT INTO DB
			rss.insert_one(entry)
			# print(feed.entries[i].title)

		i = i + 1