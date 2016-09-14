import requests, sys
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

def getCourseCodeList(url):
    result = requests.get(url)
    return [course['code'] for course in result.json()['course']]

def getCourse(url):
    result = requests.get(url)
    return Course(result.json()['course'])

def getCourses():
    baseUrl = "http://www.ime.ntnu.no/api/course/en/"
    courseCodes = getCourseCodeList(baseUrl + "-")
    courses = {}
    numberOfCourses = len(courseCodes)
    i = 1
    for code in courseCodes:
        if "-" in code: continue #An error in the API makes certain new courses unreachable
        courses[code] = getCourse(baseUrl + code)
        sys.stdout.write("\rDownloading subject %d/%d" % (i, numberOfCourses))
        i += 1
        if i > 20:
            break
    return courses
