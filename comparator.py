import sys, time
from comparators import *

comparators = [levenshtein_name, vsm_desc] #Add comparators from the comparators/ folder here
weights = [0.5, 0.5]

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
      score = 0
      for i in range(len(self.scores)):
         score += self.scores[i] * weights[i]
      return score / float(len(self.scores))

   def addReport(self, comparator, report):
      report = "Details from " + comparator + ":\n" + report + "\n"
      self.reports.append(report)

   def printExplanation(self):
      for report in self.reports:
         print(report)
      print("#############\n")

def compareToOneCourse(course1, course2):
   comparison = Comparison(course1, course2)
   comparison.compare(comparators)
   return comparison

def compareToAllCourses(courses, course, filtering, doPrint=True):
   time = -1

   #Start human-guided cluster selection 
   if filtering:
      print(course.data['code'], course.data['name'])
      courses, time = human_cluster_selection(courses)
      courses[course.data['code']] = course
      course = course.data['code']
   
   comparisons = []
   courseCodes = list(courses.keys())
   numberOfCourses = len(courses)

   #Perform comparisons
   for i in range(numberOfCourses):
      code = courseCodes[i]
      if course == code:
         continue
      if doPrint:
         sys.stdout.write("\rComparison with course %d/%d" % (i+1, numberOfCourses))

      comparison = Comparison(courses[course], courses[code])
      comparison.compare(comparators)
      comparisons.append(comparison)
   print()

   #Sort the results
   comparisons = sorted(comparisons, key=lambda x: x.getScore(), reverse=True)
   
   return comparisons, time

def human_cluster_selection(clusters):
   courses = []
   start = time.time()
   for i in range(len(clusters[0])):
      cluster = clusters[0][i]
      label = clusters[1][i]
      print("Cluster ", i+1, ":", sep="")
      print("\n\tLabel:" + label)
      print()
      include = input("Should this cluster be included? (Y/N): ")
      if include.lower() == "y":
         courses += cluster
   end = time.time()

   coursesDict = {}
   for course in courses:
      coursesDict[course.data['code']] = course
   return coursesDict, end-start

   
