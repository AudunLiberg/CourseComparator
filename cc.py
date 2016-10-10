import sys
from courses import getCourses
from comparator import compareToOneCourse, compareToAllCourses
from tests import runTests

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
    verbose = "-v" in arguments
    test = "-t" in arguments
    language = arguments[arguments.index("-l")+1] if "-l" in arguments else "en"
    courses = getCourses(redownload, language)
    course1 = arguments[1] if len(arguments) > 1 and arguments[1] in courses else None
    course2 = arguments[2] if len(arguments) > 2 and arguments[2] in courses else None
    mode = determineMode(course1, course2)
    
    if mode == "compare":
        comparison = compareToOneCourse(courses[course1], courses[course2])
        if verbose:
            comparison.printExplanation()
        print(course1, "and", course2, "have a", comparison.getScore()*100, "% match.")
    elif mode == "find-equal":
        comparisons = compareToAllCourses(courses, course1)

        #Print similarity in descending order
        print("\n\nMost similar courses to", course1 + ":")
        for comparison in comparisons[:numMatchesToDisplay]:
            print("%-12s %-12s" % (comparison.course2.data['code'], comparison.getScore()))
            if verbose:
                comparison.printExplanation()

    if test:
        runTests(courses)

if __name__ == "__main__":
    main(sys.argv)
