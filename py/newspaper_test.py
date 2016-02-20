from newspaper import Article

url = u'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'

article = Article(url)
article.download()

article.html
article.parse()

article.authors

article.publish_date
datetime.datetime(2013, 12, 30, 0, 0)

article.text

article.top_image

article.movies
article.nlp()

article.keywords

article.summary

## THINGS WE NEED
# source 
# url
# title
# date
# summary
# keywords

import newspaper
from newspaper import Article

cnn_paper = newspaper.build(u'http://cnn.com')

for article in cnn_paper.articles:
    print(article.url)

for category in cnn_paper.category_urls():
    print(category)

cnn_article = cnn_paper.articles[0]
cnn_article.download()
cnn_article.parse()
cnn_article.nlp()

from newspaper import fulltext

html = requests.get(...).text
text = fulltext(html)