import sys, time
from courses import getCourses
from comparator import compareToOneCourse, compareToAllCourses
from clusterer import cluster
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
    recluster = "-c" in arguments
    verbose = "-v" in arguments
    test = "-t" in arguments
    filtering = "-nf" not in arguments
    language = arguments[arguments.index("-l")+1] if "-l" in arguments else "en"
    courses = getCourses(redownload, language)
    course1 = arguments[1] if len(arguments) > 1 and arguments[1] in courses else None
    course2 = arguments[2] if len(arguments) > 2 and arguments[2] in courses else None
    mode = determineMode(course1, course2)
    if filtering:
        filteredCourses = cluster(courses, recluster)
        if course1:
            course1 = courses[course1]
        courses = filteredCourses
        clusters = courses[0]
        labels = courses[1]

    if mode == "compare":
        comparison = compareToOneCourse(courses[course1], courses[course2])
        if verbose:
            comparison.printExplanation()
        print(course1, "and", course2, "have a", comparison.getScore(), "% match.")
    elif mode == "find-equal":
        comparisons, time = compareToAllCourses(courses, course1, filtering)

        #Print similarity in descending order
        print("\n\nMost similar courses to", (course1 if not filtering else course1.data['code']) + ":")
        for comparison in comparisons[:numMatchesToDisplay]:
            print("%-12s %-12s" % (comparison.course2.data['code'], comparison.getScore()))
            if verbose:
                comparison.printExplanation()

    if test:
        runTests(courses, filtering)

if __name__ == "__main__":
    main(sys.argv)
