from sklearn.datasets import fetch_20newsgroups
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.cluster import KMeans, MiniBatchKMeans
import sys, random
from time import time
import numpy as np

def cluster(courses):
   use_hashing = False
   use_idf = False
   n_features = 10000
   n_components = 10
   verbose = False
   minibatch = False

   if use_hashing:
       if use_idf:
           hasher = HashingVectorizer(n_features=n_features,
                                      stop_words='english', non_negative=True,
                                      norm=None, binary=False)
           vectorizer = make_pipeline(hasher, TfidfTransformer())
       else:
           vectorizer = HashingVectorizer(n_features=n_features,
                                          stop_words='english',
                                          non_negative=False, norm='l2',
                                          binary=False)
   else:
       vectorizer = TfidfVectorizer(max_df=0.5, max_features=n_features,
                                    min_df=2, stop_words='english',
                                    use_idf=use_idf)

   # Number of clusters
   true_k = 10

   # Fill dataset with courses
   dataset = []
   labels = []
   course_list = []
   u = 0
   for code in iter(sorted(courses.keys())):
      u+=1
      course = courses[code]
      description = course.data['name'] + ". "
      if 'infoType' in course.data:
         interestingInfoCodes = ["INNHOLD", "MÅL"]
         for info in course.data['infoType']:
            if info['code'] in interestingInfoCodes and 'text' in info:
               description += info['text'] + " "

      # Remove some extremely common words from the corpus
      description = description.replace("student", "").replace("students", "").replace("candidate", "").replace("candidates", "").replace("able", "").replace("skills", "").replace("should", "").replace("shall", "")
      dataset.append(description)
      labels.append(u % true_k)      
      course_list.append(code)

   X = vectorizer.fit_transform(dataset)

   # Dimensionality reduction using LSA
   if n_components:
       t0 = time()
       svd = TruncatedSVD(n_components)
       normalizer = Normalizer(copy=False)
       lsa = make_pipeline(svd, normalizer)
       X = lsa.fit_transform(X)
       explained_variance = svd.explained_variance_ratio_.sum()

   if minibatch:
       km = MiniBatchKMeans(n_clusters=true_k, init='k-means++', n_init=1,
                            init_size=1000, batch_size=1000, verbose=verbose)
   else:
       km = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1,
                   verbose=verbose)

   km.fit(X)

   # Put result into clusters
   clusters = [[] for _ in range(true_k)]
   for i in range(len(course_list)):
      course = courses[course_list[i]]
      cluster = km.labels_[i]
      clusters[cluster].append(course)


   # Create labels using top index-terms
   topTerms = []
   for cluster in clusters:
      terms = []
      for course in cluster:
         keywords = []
         for keyword in course.keywords:
            if len(keyword) > 2 and "master" not in keyword:
               keywords.append(keyword)
         terms += keywords
      data = Counter(terms)
      label = ""
      for term in data.most_common(10):
         label += " " + term[0]
      print(label)
      topTerms.append(label)

   # Draw a Voronoi diagram
   try:
      Y = X.toarray()
   except:
      Y = X.tolist()
      
   reduced_data = PCA(n_components=2).fit_transform(Y)
   kmeans = KMeans(init='k-means++', n_clusters=true_k, n_init=10)
   kmeans.fit(reduced_data)

   h = .001 
   x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
   y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
   xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

   Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])
   Z = Z.reshape(xx.shape)
   p = plt.figure(1)
   plt.clf()
   plt.imshow(Z, interpolation='nearest',
              extent=(xx.min(), xx.max(), yy.min(), yy.max()),
              cmap=plt.cm.Paired,
              aspect='auto', origin='lower')

   plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
   
   centroids = kmeans.cluster_centers_
   plt.scatter(centroids[:, 0], centroids[:, 1],
               marker='x', s=169, linewidths=3,
               color='w', zorder=10)

   ax = p.add_subplot(111)
   plt.xlim(x_min, x_max)
   plt.ylim(y_min, y_max)
   plt.xticks(())
   plt.yticks(())
   plt.show()

   return (clusters, topTerms)

