import re

def stripHTML(text):
   return re.sub('<[^<]+?>', '', text)

def stripWhitespace(text):
   return text.strip("\r\n\t")

def cleanText(text):
   return stripWhitespace(stripHTML(text))
