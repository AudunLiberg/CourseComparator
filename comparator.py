def compare(course1, course2):
   ensemble = []

   scores = []
   for comparator in ensemble:
      score = comparator(course1, course2)
      scores.append(score)

   #Return the avarage score
   return sum(scores) / float(len(scores))
   
