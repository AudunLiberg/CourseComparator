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
   
