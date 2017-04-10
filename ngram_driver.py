from ngram_articles import ngrams
import sys
import codecs
from textblob import TextBlob as tb
from collections import defaultdict

s=sys.argv
corpus_article_list=codecs.open(s[1],'r',encoding='utf-8')
output_articles=codecs.open(s[2], 'w', encoding='utf-8')
ngram=s[3]
corpus_articles=[]
for corpus_article in corpus_article_list:
	corpus_article=tb(corpus_article)
	corpus_article=corpus_article.ngrams(n=int(ngram))
	ngram_obj=ngrams(corpus_article)
	corpus_article=ngram_obj.get_string_from_ngrams()
	output_articles.write(corpus_article)
	output_articles.write("\n")


