def compare(course1, course2):
   return len(set(course1.keywords) & set(course2.keywords)) / max(len(course1.keywords), len(course2.keywords))
