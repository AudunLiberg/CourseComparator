def compare(course1, course2):
   sharedWords = set(course1.keywords) & set(course2.keywords)
   score = 1 if len(sharedWords) >= 15 else 0
   report = "Common index-terms: " + str(sharedWords)
   return score, report
