import time, sys, os
from comparator import compareToAllCourses
from random import Random

def runTests(courses, filtering):
   # Partition courses into a development and a validation set
   clusters = False
   if filtering:
      clusters = courses
      courses = {}
      for i in range(len(clusters[0])):
         for course in clusters[0][i]:
            courses[course.data['code']] = course
   
   courseList = list(courses.keys())
   courseList.sort()
   Random(42).shuffle(courseList)
      
   size = len(courses)
   limit = int(0.8*size + 1)
   developmentTestSet = courseList[:limit]
   validationTestSet = courseList[limit:]

   dPrecisions, dRecalls, dFs, dAveragePrecisions, dTime, dFilteringTimes, dComparisons = runTestSet(developmentTestSet, courses, 10, clusters)
   vPrecisions, vRecalls, vFs, vAveragePrecisions, vTime, vFilteringTimes, vComparisons = runTestSet(validationTestSet, courses, 20, clusters)
   
   print("-------")
   print("Development set performance:")
   printMetrics(dPrecisions, dRecalls, dFs, dAveragePrecisions)
   print("\n\nValidation set performance:")
   printMetrics(vPrecisions, vRecalls, vFs, vAveragePrecisions)
   print("& ", round(sum(dPrecisions)/len(dPrecisions), 3), " & ", round(sum(dRecalls)/len(dRecalls),3) ," & ", round(sum(dFs)/len(dFs),3) ," & ",round(sum(dAveragePrecisions)/len(dAveragePrecisions),3)," & & ",round(sum(vPrecisions)/len(vPrecisions),3), " & ", round(sum(vRecalls)/len(vRecalls),3) ," & ", round(sum(vFs)/len(vFs),3) ," & ",round(sum(vAveragePrecisions)/len(vAveragePrecisions),3)," \\\\", sep="")
   if filtering:
      dFilteringTime = sum(dFilteringTimes)
      vFilteringTime = sum(vFilteringTimes)
      print("Development filtering time:", round(dFilteringTime, 1))
      print("Development comparison time:", round(dTime - dFilteringTime, 1))
      print("Number of courses filtered: ", size - dComparisons, " (", dComparisons/size, ")", sep="")
      print("Validation filtering time:", round(vFilteringTime, 1))
      print("Validation comparison time:", round(vTime - vFilteringTime, 1))
      print("Number of courses filtered: ", size - vComparisons, " (", vComparisons/size, ")", sep="")
   else:
      print("Development time:", round(dTime, 1))
      print("Validation time:", round(vTime, 1))


def runTestSet(tests, courses, limit, clusters):
   start = time.time()
   numberOfTests = 0
   averagePrecisions = []
   precisions = []
   recalls = []
   Fs = []
   filteringTimes = []
   averageComparisons = []

   n_tests_performed = 0
   print("%-12s %-12s %-12s %-12s " % ("Course", "Recall", "Precision", "F-Measure"))
   for code in tests:
      if n_tests_performed == limit:
         break
      course = courses[code]
      if len(course.tests) > 0:
         numberOfTests += 1

         # Collect comparisons with a score no worse than 0.05
         comparisons = []
         comparisonArgument = clusters if clusters else courses
         courseArgument = course if clusters else code
         firstComparisons, filteringTime = compareToAllCourses(comparisonArgument, courseArgument, clusters != False, False)

         for comparison in firstComparisons:
            if comparison.getScore() < 0.05:
               continue
            comparisons.append(comparison.course2.data['code'])

         comparisons = comparisons[:10]
         
         correct = len(set(course.tests) & set(comparisons))
         total = len(course.tests)

         # Calculate result quality measures
         precision = 0.0 if len(comparisons) == 0 else correct / len(comparisons)
         recall = correct / total
         F = 0.0 if recall + precision == 0 else (2 * precision * recall) / (recall + precision)

         rank = 1
         correctSoFar = 0
         precisionAtRank = []
         for comparison in comparisons:
            if comparison in course.tests:
               correctSoFar += 1
               precisionAtRank.append(correctSoFar/rank)
            rank += 1
            
         averagePrecision = 0 if len(precisionAtRank) == 0 else sum(precisionAtRank)/len(precisionAtRank)
         averagePrecisions.append(averagePrecision)
         precisions.append(precision)
         recalls.append(recall)
         Fs.append(F)
         filteringTimes.append(filteringTime)
         n_tests_performed += 1
         averageComparisons.append(len(firstComparisons))

         # Clear command window if filtering
         if clusters:
            clear = lambda: os.system('cls')
            clear()
         
         print("%-12s %-12s %-12s %-12s %-12s %-12s" % (code, str(round(recall, 3)), str(round(precision, 3)), str(round(F, 3)), str(correct), str(total)))

   end = time.time()
   timeSpent = end - start
   return precisions, recalls, Fs, averagePrecisions, timeSpent, filteringTimes, sum(averageComparisons)/len(averageComparisons)

def printMetrics(precisions, recalls, Fs, averagePrecisions):
   print("Average Precision:", sum(precisions)/len(precisions))
   print("Average Recall:", sum(recalls)/len(recalls))
   print("Average F-Measure:", sum(Fs)/len(Fs))
   print("Mean Average Precision (MAP):", sum(averagePrecisions)/len(averagePrecisions))
