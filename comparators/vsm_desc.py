def compare(course1, course2):
   sharedKeywords = set(course1.keywords) & set(course2.keywords)
   keywords = set(course1.keywords + course2.keywords)
   unionLength = len(set(course1.keywords) | set(course2.keywords))

   v1 = []
   v2 = []
   for keyword in keywords:
      v1.append(course1.termFrequency[keyword] / course1.documentFrequency[keyword])
      v2.append(course2.termFrequency[keyword] / course2.documentFrequency[keyword])

   length1 = (sum([(course1.termFrequency[keyword] / course1.documentFrequency[keyword])**2 for keyword in keywords]))**0.5
   length2 = (sum([(course2.termFrequency[keyword] / course2.documentFrequency[keyword])**2 for keyword in keywords]))**0.5
   dotproduct = sum([v1[i] * v2[i] for i in range(len(v1))])

   report = "Vector Space Model similarity:\n" + str(sharedKeywords) + "\n" + str(dotproduct) + "\n" + str(length1 * length2)
   score = dotproduct / (length1 * length2) if len(v1) > 0 else 0
   return score, report
