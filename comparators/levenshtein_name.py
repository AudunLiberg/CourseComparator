#import Levenshtein
import math

def compare(course1, course2):
   distances = []
   commonLettersFraction = len(set(course1.data["name"]) & set(course2.data["name"])) / (len(set(course1.data["name"]) | set(course2.data["name"])))
   if commonLettersFraction < 0.6:
      return 0, ""
   return 1/ (math.log(levenshtein(course1.data["name"], course2.data["name"]) + 1) + 1), ""

   keywords1 = sorted(course1.keywords)
   keywords2 = sorted(course2.keywords)

   indexIn2 = 0;
   for keyword in keywords1:
      for i in range(indexIn2, len(keywords2)):
         distances.append(levenshtein(keyword, similarKeyword))
   
   
   prefixes = {}
   for keyword in course1.keywords:
      prefix = keyword[:2] 
      if prefix in prefixes:
         prefixes[prefix].append(keyword)
      else:
         prefixes[prefix] = [keyword]

   for keyword in course2.keywords:
      prefix = keyword[:2]
 
            
  

   meanDistance = 0 if len(distances) == 0 else sum(distances) / len(distances)
   report = "Mean Levenshtein distance: " + str(meanDistance)
   return meanDistance, report

def levenshtein(a,b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a,b = b,a
        n,m = m,n
        
    current = range(n+1)
    for i in range(1,m+1):
        previous, current = current, [i]+[0]*n
        for j in range(1,n+1):
            add, delete = previous[j]+1, current[j-1]+1
            change = previous[j-1]
            if a[j-1] != b[i-1]:
                change = change + 1
            current[j] = min(add, delete, change)
            
    return current[n]
