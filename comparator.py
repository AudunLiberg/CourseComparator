import sys
from comparators import *

fastEnsemble = [equalkeywords]
slowEnsemble = []
slowEnsembleLimit = 50

def getModuleName(module):
   return module.__name__.split(".")[1]

class Comparison:
   
   def __init__(self, course1, course2):
      self.course1 = course1
      self.course2 = course2
      self.reports = []
      self.scores = []

   def compare(self, ensemble):
      for comparator in ensemble:
         score, report = comparator.compare(self.course1, self.course2)
         self.addReport(getModuleName(comparator), report)
         self.scores.append(score)

   def getScore(self):
      return sum(self.scores) / float(len(self.scores))

   def addReport(self, comparator, report):
      report = "Details from " + comparator + ":\n" + report + "\n"
      self.reports.append(report)

   def printExplanation(self):
      for report in self.reports:
         print(report)
      print("#############\n")

def compareToOneCourse(course1, course2):
   comparison = Comparison(course1, course2)
   comparison.compare(fastEnsemble)
   comparison.compare(slowEnsemble)
   return comparison

def compareToAllCourses(courses, course, doPrint=True):
   comparisons = []
   courseCodes = list(courses.keys())
   numberOfCourses = len(courses)

   #Perform comparisons from the fast ensemble
   for i in range(numberOfCourses):
      code = courseCodes[i]
      if course == code:
         continue
      if doPrint:
         sys.stdout.write("\rStep 1: Fast comparison with course %d/%d" % (i+1, numberOfCourses))
      comparison = Comparison(courses[course], courses[code])
      comparison.compare(fastEnsemble)
      comparisons.append(comparison)
   print()

   #Sort the results and pick out the n best ones
   comparisons = sorted(comparisons, key=lambda x: x.getScore(), reverse=True)[:slowEnsembleLimit]

   #Perform comparisons from the slow ensemble
   for i, comparison in enumerate(comparisons):
      if doPrint:
         sys.stdout.write("\rStep 2: Slow comparison with course %d/%d" % (i+1, slowEnsembleLimit))
      comparison.compare(slowEnsemble)
   
   return comparisons


   
