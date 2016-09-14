import sys
from courses import getCourses

def main(arguments):
    redownload = "-r" in arguments
    courses = getCourses(redownload)

if __name__ == "__main__":
    main(sys.argv)
