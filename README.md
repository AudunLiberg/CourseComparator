# CourseComparator
A comparator designed to find similar courses within the Norwegian University of Science and Technology’s extensive course catalogue. The CourseComparator utilizes an ensemble of classical information retrieval and natural language processing techniques.

## Requirements

* [nltk](http://www.nltk.org/)

## Usage
Run the program through `cc.py`. Supplying a course code as an argument will find the best matches for that course. Supplying two codes will compare those two particular courses. Example input:

* `python cc.py TDT4100`
* `python cc.py TMA4100 MA1101`