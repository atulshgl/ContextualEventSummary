from tf_idf import calculate_tfidf
from ngram_articles import ngrams
import math
import sys
import json
import codecs
from textblob import TextBlob as tb
from collections import defaultdict

s=sys.argv
text_file=codecs.open(s[1],'r',encoding='utf-8')
out_file=codecs.open(s[2], 'w', encoding='utf-8')
corpus_article_list=codecs.open(s[3],'r',encoding='utf-8')
ngram=s[4]


article_list=[]
corpus_articles=[]
count=0
for article in text_file:
	count+=1
	article=tb(article)
	article=article.ngrams(n=int(ngram))
	ngram_obj=ngrams(article)
	article=ngram_obj.get_string_from_ngrams()
	article=tb(article)
	article_list.append(article)

for corpus_article in corpus_article_list:
	corpus_article=tb(corpus_article)
	corpus_articles.append(corpus_article)


tf_idf_scores=defaultdict(lambda:{})
article_count=0
for i, article in enumerate(article_list):
	article_count+=1
	#print("Top words in article {}".format(i + 1))
	scores={}
	for word in article.words:
		tfidf_obj=calculate_tfidf(word,article,corpus_articles)
		scores[word]= tfidf_obj.tfidf()
	tf_idf_scores["article"+str(article_count)]=scores
	#scores = {word: tfidf(word, article, corpus_articles) for word in article.words}
	#tf_idf_scores["article"+str(article_count)]=scores
json.dump(tf_idf_scores,out_file,ensure_ascii=False)


