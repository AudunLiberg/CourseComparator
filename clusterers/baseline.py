import sys, requests
from time import time

def cluster(courses):
   facultyMapping = {832: 'Faculty of Information Technology and Electrical Engineering', 773: 'Education Quality Division', 834: 'Faculty of Engineering', 1181: 'Faculty of Economics and Management', 1186: 'Faculty of Social and Educational Sciences', 1222: 'Faculty of Social and Educational Sciences', 807: 'Faculty of Architecture and Design', 1223: 'Faculty of Social and Educational Sciences', 814: 'Faculty of Humanities', 821: 'Faculty of Humanities', 822: 'Faculty of Humanities', 823: 'Faculty of Humanities', 1080: 'Faculty of Humanities', 1081: 'Faculty of Humanities', 1082: 'Faculty of Humanities', 827: 'Faculty of Information Technology and Electrical Engineering', 828: 'Faculty of Information Technology and Electrical Engineering', 829: 'Faculty of Information Technology and Electrical Engineering', 830: 'Faculty of Information Technology and Electrical Engineering', 1215: 'Faculty of Information Technology and Electrical Engineering', 1216: 'Faculty of Engineering', 1217: 'Faculty of Engineering', 1218: 'Faculty of Engineering', 1219: 'Faculty of Engineering', 1220: 'Faculty of Engineering', 838: 'Faculty of Engineering', 839: 'Faculty of Engineering', 840: 'Faculty of Architecture and Design', 843: 'Faculty of Engineering', 825: 'Faculty of Information Technology and Electrical Engineering', 1102: 'Faculty of Medicine and Health Sciences', 849: 'Faculty of Medicine and Health Sciences', 851: 'Faculty of Medicine and Health Sciences', 852: 'Faculty of Medicine and Health Sciences', 853: 'Faculty of Medicine and Health Sciences', 854: 'Faculty of Medicine and Health Sciences', 855: 'Faculty of Medicine and Health Sciences', 863: 'Faculty of Natural Sciences', 865: 'Faculty of Natural Sciences', 866: 'Faculty of Natural Sciences', 867: 'Faculty of Natural Sciences', 868: 'Faculty of Natural Sciences', 869: 'Faculty of Natural Sciences', 870: 'Faculty of Natural Sciences', 871: 'Faculty of Social and Educational Sciences', 873: 'Faculty of Social and Educational Sciences', 1130: 'Faculty of Medicine and Health Sciences', 876: 'Faculty of Social and Educational Sciences', 877: 'Faculty ofEconomics and Management', 1134: 'Faculty of Natural Sciences', 879: 'Faculty of Social and Educational Sciences', 880: 'Faculty ofSocial and Educational Sciences', 881: 'Faculty of Economics and Management', 1138: 'Faculty of Economics and Management', 831: 'Faculty of Information Technology and Electrical Engineering'}
   
   faculties = {}
   
   for code in courses:
      course = courses[code]
      institute = course.data['ouId']
      faculty = facultyMapping[institute]

      # Correct a couple of spelling mistakes in the API
      if faculty == "Faculty ofEconomics and Management":
         faculty = "Faculty of Economics and Management"
      if faculty == "Faculty ofSocial and Educational Sciences":
         faculty = "Faculty of Social and Educational Sciences"

      if faculty == "Education Quality Division":
         print (code)

      if faculty not in faculties:
         faculties[faculty] = [course]
      else:
         faculties[faculty].append(course)

   # Sort courses into clusters and apply labels
   labels = []
   clusters = []
   for faculty in faculties:
      courses = faculties[faculty]
      clusters.append(courses)
      labels.append(faculty)

   return (clusters, labels)
