import re

def stripHTML(text):
   return re.sub('<[^<]+?>', '', text)

def stripWhitespace(text):
   whitespace = "\r\n\t"
   return text

def cleanText(text):
   return stripWhitespace(stripHTML(text))
