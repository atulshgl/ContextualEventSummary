class ngrams(object):
	def __init__(self, corpus_article):
		'''
		Initialise object with single corpus article
		:param = corpus article

		'''
		self.article=corpus_article

	def get_string_from_ngrams(self):
		"""
		Creates new article with n gram initialised in ngram_driver
		:return= updated article  

		"""
		new_article=""
		for ngrams in self.article:
			temp=""
			for word in ngrams:
				word.encode(encoding='UTF-8',errors='strict')
				temp=temp+word+"/"
			temp=temp[:-1]
			new_article=new_article+temp+" "
		new_article=new_article[:-1]
		return new_article


