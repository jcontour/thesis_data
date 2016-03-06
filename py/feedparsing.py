from bs4 import BeautifulSoup
from alchemyapi import AlchemyAPI
import pymongo
import feedparser
import nltk
from nltk.corpus import stopwords

alchemyapi = AlchemyAPI() 

connection = pymongo.MongoClient("mongodb://localhost")
db = connection.thesis
nyt = db.nyt

feeds = [ {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml'}, {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml'}, {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/InternationalBusiness.xml'}, {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml'}, {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml'}, {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml'}, {'category': 'world', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml'}, {'category': 'us', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/US.xml'},  {'category': 'us', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Education.xml'},  {'category': 'us', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml'},  {'category': 'us', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Business.xml'},  {'category': 'politics', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml'}, {'category': 'tech', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml'}, {'category': 'tech', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml'}, {'category': 'tech', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml'}, {'category': 'tech', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/PersonalTech.xml'}, {'category': 'science', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml'}, {'category': 'science', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Science.xml'}, {'category': 'science', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Environment.xml'}, {'category': 'science', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Space.xml'}, {'category': 'sports', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Sports.xml'}, {'category': 'health', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Health.xml'}, {'category': 'culture', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Television.xml'}, {'category': 'culture', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Movies.xml'}, {'category': 'arts', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/Arts.xml'}, {'category': 'arts', 'url': 'http://rss.nytimes.com/services/xml/rss/nyt/ArtandDesign.xml'} ]

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
			entry = {'category': source['category'], 'title': feed.entries[i].title, 'link': feed.entries[i].link, 'description': desc, 'date': feed.entries[i].published, 'keywords': keywords}
			# INSERT INTO DB
			nyt.insert_one(entry)
			# print(feed.entries[i].title)

		i = i + 1