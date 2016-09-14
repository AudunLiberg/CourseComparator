import requests, sys, os, pickle
from stringUtil import cleanText

class Course:
   def __init__(self, data):
      self.data = data
      self.setDescription()

   def setDescription(self):
      self.description = self.data['name'] + ". "
      if not 'infoType' in self.data:
         return #Some courses does not have any information in the API
      interestingInfoCodes = ["INNHOLD", "LÆRFORM", "MÅL"]
      for info in self.data['infoType']:
         if info['code'] in interestingInfoCodes and 'text' in info:
            self.description += cleanText(info['text']) + " "

def isPickled():
   return os.path.isdir("data")

def getCourseCodeList(url):
    result = requests.get(url)
    return [course['code'] for course in result.json()['course']]

def getCourse(url):
    result = requests.get(url)
    try:
       return Course(result.json()['course'])
    except ValueError:
       return None

def getCourses(redownload):
    if redownload and isPickled():
       os.remove("data/courses.p")
       os.rmdir("data")
   
    if isPickled():
       return pickle.load(open("data/courses.p", "rb"))
    else:
       baseUrl = "http://www.ime.ntnu.no/api/course/en/"
       courseCodes = getCourseCodeList(baseUrl + "-")
       courses = {}
       numberOfCourses = len(courseCodes)
       i = 1
       for i in range(numberOfCourses):
           code = courseCodes[i]
           courses[code] = getCourse(baseUrl + code)
           sys.stdout.write("\rDownloading subject %d/%d" % (i, numberOfCourses))

       #Pickle the courses for faster access later
       os.makedirs("data")
       pickle.dump(courses, open("data/courses.p", "wb" ))
       return courses
