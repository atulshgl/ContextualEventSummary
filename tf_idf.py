# -*- coding: UTF-8 -*-
import math
import sys
import json
import codecs
from textblob import TextBlob as tb
from collections import defaultdict

# Calculate Term Frequency, # of times "word" exists in "article"
def tf(word, article):
	return float(article.words.count(word)) / len(article.words)

# Calculate number of "articles" containing "word"
def n_containing(word, article_list):
	return sum(1 for article in article_list if word in article.words)

# Calculate how common a "word" is among all "articles"
def idf(word, article_list):
	return math.log(float(len(article_list)) / (1 + n_containing(word, article_list)))

# Calculate  TF-IDF score
def tfidf(word, article, article_list):
	return tf(word, article) * idf(word, article_list)


# Create String out of n grams
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
text_file=codecs.open(s[1],'r',encoding='utf-8')
out_file=codecs.open(s[2], 'w', encoding='utf-8')
ngram=s[3]

article_list=[]
count=0
for article in text_file:
	count+=1
	article=tb(article)
	article=article.ngrams(n=int(ngram))
	article=get_string_from_ngrams(article)
	article=tb(article)
	article_list.append(article)

tf_idf_scores=defaultdict(lambda:{})
article_count=0
for i, article in enumerate(article_list):
	article_count+=1
	#print("Top words in article {}".format(i + 1))
	scores = {word: tfidf(word, article, article_list) for word in article.words}
	tf_idf_scores["article"+str(article_count)]=scores
json.dump(tf_idf_scores,out_file,ensure_ascii=False)
