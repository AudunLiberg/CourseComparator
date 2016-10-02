import sys
from comparators import *

def getModuleName(module):
   return module.__name__.split(".")[1]

class Comparison:
   
   def __init__(self, course1, course2):
      self.course1 = course1
      self.course2 = course2
      self.reports = []

   def addReport(self, comparator, report):
      report = "Details from " + comparator + ":\n" + report + "\n"
      self.reports.append(report)

   def printExplanation(self):
      for report in self.reports:
         print(report)
      print("#############\n")

def compareToAllCourses(courses, course, doPrint=True):
   comparisons = []
   courseCodes = list(courses.keys())
   numberOfCourses = len(courses)
   for i in range(numberOfCourses):
      code = courseCodes[i]
      if course == code:
         continue
      if doPrint:
         sys.stdout.write("\rComparing with course %d/%d" % (i+1, numberOfCourses))
      comparisons.append(compare(courses[course], courses[code]))
   return sorted(comparisons, key=lambda x: x.score, reverse=True)

def compare(course1, course2):
   ensemble = [equalkeywords]

   scores = []
   comparison = Comparison(course1, course2)
   for comparator in ensemble:
      score, report = comparator.compare(course1, course2)
      comparison.addReport(getModuleName(comparator), report)
      scores.append(score)

   comparison.score = sum(scores) / float(len(scores))
   return comparison
   
