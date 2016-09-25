import requests, sys, os, pickle, glob
from stringUtil import cleanText
from collections import Counter
from operator import itemgetter
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.data import load as nltk_load
from nltk.stem.wordnet import WordNetLemmatizer

class Course:

   wordFrequency = Counter()
   lemmatizer = WordNetLemmatizer()
   
   def __init__(self, data):
      self.data = data
      self.setDescription()
      self.tokenize()
      self.countWords()

   def setDescription(self):
      self.description = self.data['name'] + ". "
      if not 'infoType' in self.data:
         return #Some courses does not have any information in the API
      interestingInfoCodes = ["INNHOLD", "LÆRFORM", "MÅL"]
      for info in self.data['infoType']:
         if info['code'] in interestingInfoCodes and 'text' in info:
            self.description += cleanText(info['text']) + " "

   def tokenize(self):
      sentenceDetector = nltk_load('tokenizers/punkt/english.pickle')
      sentences = sentenceDetector.tokenize(self.description.strip())
      self.sentences = []
      self.sentencesWithoutStopwords = []
      for sentence in sentences:
         tokens = word_tokenize(sentence)
         tokensWithoutStopwords = [word for word in tokens if word.lower() not in stopwords.words('english')]
         self.sentences.append(tokens)
         self.sentencesWithoutStopwords.append(tokensWithoutStopwords)

   def countWords(self):
      for sentence in self.sentencesWithoutStopwords:
         for word in sentence:
            self.wordFrequency[self.lemmatizer.lemmatize(word.lower())] += 1

   def determineKeywords(self):
      wordsByRarity = {}
      for sentence in self.sentencesWithoutStopwords:
         for word in sentence:
            word = self.lemmatizer.lemmatize(word.lower())
            wordsByRarity[word] = self.wordFrequency[word]

      wordsByRarity = sorted(wordsByRarity.items(), key=itemgetter(1))
      numKeywords = min(len(wordsByRarity), 30)
      self.keywords = [keyword[0] for keyword in wordsByRarity[:numKeywords]]

def isPickled():
   return os.path.isdir("data")

def getCourseCodeList(url):
    result = requests.get(url)
    return [course['code'] for course in result.json()['course']]

def getCourseData(url):
    result = requests.get(url)
    return result.json()['course']

def getCourses(redownload):
    if redownload and isPickled():
       files = glob.glob('data/*')
       for file in files:
          os.remove(file)
       os.rmdir("data")
   
    if isPickled():
       Course.wordFrequency = pickle.load(open("data/wordfrequency.p", "rb"))
       return pickle.load(open("data/courses.p", "rb"))
    else:
       baseUrl = "http://www.ime.ntnu.no/api/course/en/"
       courseCodes = getCourseCodeList(baseUrl + "-")
       courses = {}
       numberOfCourses = len(courseCodes)
       for i in range(numberOfCourses):
           code = courseCodes[i]
           courseData = getCourseData(baseUrl + code)
           if courseData != None:
              courses[code] = Course(courseData)
           sys.stdout.write("\rDownloading subject %d/%d" % (i, numberOfCourses))
            
       for code in courses:
          courses[code].determineKeywords()

       #Pickle the courses for faster access later
       os.makedirs("data")
       pickle.dump(courses, open("data/courses.p", "wb" ))
       pickle.dump(Course.wordFrequency, open("data/wordfrequency.p", "wb" ))
       return courses
