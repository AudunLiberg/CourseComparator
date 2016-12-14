def compare(course1, course2):
   sharedKeywords = set(course1.data["name"].split()) & set(course2.data["name"].split())
   unionLength = len(set(course1.data["name"].split()) | set(course2.data["name"].split()))
   report = "Jaccard index (shared index-terms): " + str(sharedKeywords) + " (" + str(unionLength) + " total)"
   score = len(sharedKeywords) / unionLength
   return score, report
