from comparator import compareToAllCourses

def runTests(courses):
   numberOfTests = 0
   scores = []
   
   for code in courses:
      course = courses[code]
      if len(course.tests) > 0:
         numberOfTests += 1
         comparisons = [comparison.course2.data['code'] for comparison in compareToAllCourses(courses, code, False)[:20]]
         correct = len(set(course.tests) & set(comparisons))
         total = len(course.tests)
         score = correct / total
         scores.append(score)
         print("%-12s %-12s %-12s" % (code, str(correct)+"/"+str(total), score))
   print("-------")
   print("Total score:", sum(scores)/numberOfTests)
