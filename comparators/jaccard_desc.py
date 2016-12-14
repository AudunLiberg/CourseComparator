def compare(course1, course2):
   sharedKeywords = set(course1.keywords) & set(course2.keywords)
   unionLength = len(set(course1.keywords) | set(course2.keywords))
   report = "Jaccard index (shared index-terms): " + str(sharedKeywords) + " (" + str(unionLength) + " total)"
   score = len(sharedKeywords) / unionLength
   return score, report
