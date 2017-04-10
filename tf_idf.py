import math
class calculate_tfidf(object):
	def __init__(self, word,article,corpus_articles):
		self.word=word
		self.article=article
		self.corpus_articles=corpus_articles

# Calculate Term Frequency, # of times "word" exists in "article"
	def tf(self):
		return float(self.article.words.count(self.word)) / len(self.article.words)

# Calculate number of "articles" containing "word"
	def n_containing(self):
		return sum(1 for article in self.corpus_articles if self.word in article.words)

# Calculate how common a "word" is among all "articles"
	def idf(self):
		return math.log(float(len(self.corpus_articles)) / (1 + self.n_containing()))

# Calculate  TF-IDF score
	def tfidf(self):
		return self.tf() * self.idf()

