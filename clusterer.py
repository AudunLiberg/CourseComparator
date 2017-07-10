import sys, pickle, time
from clusterers import *
from collections import Counter

clusteringAlgorithm = kmeans #Provide clustering algorithm from the clusterers/ folder here

def getModuleName(module):
   return module.__name__.split(".")[1]

def cluster(courses, recluster):
   path = "data/clusters/clusters.p"
   if recluster:
      clusters = clusteringAlgorithm.cluster(courses)
      pickle.dump(clusters, open(path, "wb" ))
   else:
      clusters = pickle.load(open(path, "rb"))
      
   return clusters
