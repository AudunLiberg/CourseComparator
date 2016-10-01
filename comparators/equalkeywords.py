def compare(course1, course2):
   sharedKeywords = set(course1.keywords) & set(course2.keywords)
   report = "Shared keywords: " + str(sharedKeywords)
   score = len(sharedKeywords) / max(len(course1.keywords), len(course2.keywords))
   return score, report
