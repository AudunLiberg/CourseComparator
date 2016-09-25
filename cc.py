import sys
from courses import getCourses
from comparator import compare
from operator import itemgetter

numMatchesToDisplay = 20

def determineMode(course1, course2):
    if course1 != None and course2 != None:
        return "compare"
    elif course1 != None:
        return "find-equal"
    else:
        return "error"

def main(arguments):
    redownload = "-r" in arguments
    courses = getCourses(redownload)
    course1 = arguments[1] if len(arguments) > 1 and arguments[1] in courses else None
    course2 = arguments[2] if len(arguments) > 2 and arguments[2] in courses else None
    mode = determineMode(course1, course2)
    
    if mode == "compare":
        score = compare(courses[course1], courses[course2])
        print(course1, "and", course2, "have a", score, "% match.")
    elif mode == "find-equal":
        similarity = {}
        courseCodes = list(courses.keys())
        numberOfCourses = len(courses)
        for i in range(numberOfCourses):
            code = courseCodes[i]
            if course1 == code:
                continue
            sys.stdout.write("\rComparing with course %d/%d" % (i+1, numberOfCourses))
            similarity[code] = compare(courses[course1], courses[code])

        #Print similarity in descending order
        sortedSimilarity = sorted(similarity.items(), key=itemgetter(1), reverse=True)
        print("\n\nMost similar courses to", course1 + ":")
        for course in sortedSimilarity[:numMatchesToDisplay]:
            print("%-12s %-12s" % (course[0], course[1]))

if __name__ == "__main__":
    main(sys.argv)
