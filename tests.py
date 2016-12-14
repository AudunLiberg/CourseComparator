from comparator import compareToAllCourses

def runTests(courses):
   numberOfTests = 0
   averagePrecisions = []
   precisions = []
   recalls = []
   Fs = []
   
   print("%-12s %-12s %-12s %-12s " % ("Coure", "Recall", "Precision", "F-Measure"))
   for code in courses:
      course = courses[code]
      if len(course.tests) > 0:
         numberOfTests += 1

         # Collect comparisons with a score no worse than 0.3
         comparisons = []
         for comparison in compareToAllCourses(courses, code, False):
            if comparison.getScore() < 0.3:
               break
            comparisons.append(comparison.course2.data['code'])
         
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
         
         print("%-12s %-12s %-12s %-12s " % (code, str(round(recall, 3)), str(round(precision, 3)), str(round(F, 3))))
   print("-------")
   print("Average Precision:", sum(precisions)/len(precisions))
   print("Average Recall:", sum(recalls)/len(recalls))
   print("Average F-Measure:", sum(Fs)/len(Fs))
   print("Mean Average Precision (MAP):", sum(averagePrecisions)/len(averagePrecisions))
