# -*- coding: utf-8 -*- 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
from nltk.corpus import stopwords
import os, codecs, time
start_time = time.time()

cur_dir = os.path.join(os.path.dirname(__file__))
input_file = cur_dir + 'phrases.txt'
output_file = cur_dir + 'events.txt'

def readPhrases(input_file):
    with codecs.open(input_file, 'r', 'utf-8') as f:
        phrases = f.readlines()
    return filter(None, phrases)

documents = readPhrases(input_file)

vectorizer = TfidfVectorizer(stop_words=stopwords.words('spanish'))
X = vectorizer.fit_transform(documents)

true_k = 5
model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
model.fit(X)

print("Top terms per cluster:")
order_centroids = model.cluster_centers_.argsort()[:, ::-1]
terms = vectorizer.get_feature_names()
for i in range(true_k):
    print "Cluster %d:" % i,
    for ind in order_centroids[i, :11]:
        print ' %s' % terms[ind],
    print ''

print("--- %s seconds ---" % (time.time() - start_time))
