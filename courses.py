import requests, sys, os, shutil, pickle, glob, math
from stringUtil import cleanText
from collections import Counter
from operator import itemgetter
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.data import load as nltk_load
from nltk.stem import SnowballStemmer

languages = {
   "no": "norwegian",
   "en": "english"
}

institutes = {}

class Course:

   documentFrequency = Counter()
   
   def __init__(self, data):
      self.language = languages[data["language"]]
      self.stemmer = SnowballStemmer(self.language)
      self.termFrequency = Counter()
      self.data = data
      self.setDescription()
      self.tokenize()
      self.countWords()
      self.storeInstitute()
      self.tests = []


   def setDescription(self):
      self.description = self.data['name'] + ". "
      if not 'infoType' in self.data:
         return #Some courses does not have any information in the API
      interestingInfoCodes = ["INNHOLD", "MÅL"]
      for info in self.data['infoType']:
         if info['code'] in interestingInfoCodes and 'text' in info:
            self.description += cleanText(info['text']) + " "

   def tokenize(self):
      sentenceDetector = nltk_load("tokenizers/punkt/" + self.language + ".pickle")
      sentences = sentenceDetector.tokenize(self.description.strip())
      self.sentences = []
      self.sentencesWithoutStopwords = []
      for sentence in sentences:
         tokens = word_tokenize(sentence)
         tokensWithoutStopwords = [word for word in tokens if word.lower() not in stopwords.words(self.language)]
         self.sentences.append(tokens)
         self.sentencesWithoutStopwords.append(tokensWithoutStopwords)

   def countWords(self):
      wordSet = set()
      for sentence in self.sentencesWithoutStopwords:
         for word in sentence:
            word = self.stemmer.stem(word.lower())
            self.termFrequency[word] += 1
            wordSet |= {word}
      
      for word in wordSet:
         self.documentFrequency[word] += 1

   def determineKeywords(self):
      wordsByRarity = {}
      for sentence in self.sentencesWithoutStopwords:
         for word in sentence:
            word = self.stemmer.stem(word.lower())
            wordsByRarity[word] = self.documentFrequency[word] / self.termFrequency[word]

      wordsByRarity = sorted(wordsByRarity.items(), key=itemgetter(1))
      numKeywords = min(len(wordsByRarity), 30)
      self.keywords = [keyword[0] for keyword in wordsByRarity[:numKeywords]]

   def storeInstitute(self):
      orgCode = self.data['ouId']
      if orgCode not in institutes:
         result = requests.get("http://www.ime.ntnu.no/api/org/en/" + str(orgCode)).json()
         name = result["orgUnitDetailed"]["name"]
         institutes[orgCode] = name
	

def isPickled():
   return os.path.isdir("data")

def getCourseCodeList(url):
    result = requests.get(url)
    return [course['code'] for course in result.json()['course']]

def getCourseData(url):
    try:
       result = requests.get(url).json()
       result["course"]["language"] = result["request"]["language"]
       return result["course"]
    except:
       return None

def getCourses(redownload, chosenLanguage):
    if redownload and isPickled():
       shutil.rmtree('data/')

    coursesList = {}
    if isPickled():
       Course.documentFrequency = pickle.load(open("data/" + chosenLanguage + "/documentFrequency.p", "rb"))
       Course.institutes = pickle.load(open("data/" + chosenLanguage + "/institutes.p", "rb"))
       courses = pickle.load(open("data/" + chosenLanguage + "/courses.p", "rb"))
       return courses
    else:
       baseUrl = "http://www.ime.ntnu.no/api/course/"
       courseCodes = getCourseCodeList(baseUrl + "-")
       numberOfCourses = len(courseCodes)

       for language in languages:
          courses = {}
          for i in range(numberOfCourses):
              code = courseCodes[i]
              courseData = getCourseData(baseUrl + language + "/" + code)
              if courseData != None:
                 courses[code] = Course(courseData)
              sys.stdout.write("\r(" + language.upper() + ") Downloading subject %d/%d" % (i+1, numberOfCourses))
          print()    
          for code in courses:
             courses[code].determineKeywords()
             #Use credit reduction as a basis for tests
             if 'creditReduction' in courses[code].data:
                for reduction in courses[code].data['creditReduction']:
                   if reduction['courseCode'] in courses:
                      courses[code].tests.append(reduction['courseCode'])
          
          #Pickle the courses for access later
          dataDir = "data/" + language + "/"
          os.makedirs(dataDir)
          pickle.dump(courses, open(dataDir + "courses.p", "wb" ))
          pickle.dump(Course.documentFrequency, open(dataDir + "documentFrequency.p", "wb" ))
          pickle.dump(institutes, open(dataDir + "institutes.p", "wb" ))

          coursesList[language] = courses
       return coursesList[chosenLanguage]
