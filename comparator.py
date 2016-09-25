from comparators import *

def compare(course1, course2):
   ensemble = [equalkeywords]

   scores = []
   for comparator in ensemble:
      score = comparator.compare(course1, course2)
      scores.append(score)

   #Return the avarage score
   return sum(scores) / float(len(scores))
   
