import sys
from courses import getCourses
from comparator import compare

def determineMode(course1, course2):
    if course1 != None and course2 != None:
        return "compare"
    elif course1 != None:
        return "custom-compare"
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
        print (course1, "and", course2, "have a", score, "% match.")

if __name__ == "__main__":
    main(sys.argv)
