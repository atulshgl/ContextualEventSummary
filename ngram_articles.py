# -*- coding: UTF-8 -*-
import sys
import json
import codecs
from textblob import TextBlob as tb
from collections import defaultdict


def get_string_from_ngrams(article):
	new_article=""
	for ngrams in article:
		temp=""
		for word in ngrams:
			word.encode(encoding='UTF-8',errors='strict')
			temp=temp+word+"/"
		temp=temp[:-1]
		new_article=new_article+temp+" "
	new_article=new_article[:-1]
	return new_article




s=sys.argv
corpus_article_list=codecs.open(s[1],'r',encoding='utf-8')
output_articles=codecs.open(s[2], 'w', encoding='utf-8')
ngram=s[3]
corpus_articles=[]
for corpus_article in corpus_article_list:
	corpus_article=tb(corpus_article)
	corpus_article=corpus_article.ngrams(n=int(ngram))
	corpus_article=get_string_from_ngrams(corpus_article)
	#corpus_article=tb(corpus_article)
	#print type(corpus_article)
	#print corpus_article
	output_articles.write(corpus_article)
	output_articles.write("\n")
	#corpus_articles.append(str(corpus_article))

#for article in corpus_articles:
	#output_articles.write(article+"\n")
