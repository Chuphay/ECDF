"""ECDF
Suppose you have multiple text files, each containing lines of the form:
student_id,course_name,school_name,test_date,test_score

An example valid line could look like the following (note that the files will not have headers):
9812345,”Algebra”,”Port Chester University”,2015-03-17,75.5

Write a program to compute the empirical cumulative distribution function of the average test score of students who attended a particular school, which is specified as a parameter to the program.

An example invocation of the program would be:
python ecdf.py --school “Port Chester University” input_file1.csv input_file2.csv

The expected output from invoking such a program would be of the following form (use a single tab character to delimit field values, and display the results to standard output):

Port Chester University students

percentile    mean_test_score
1                  0
2                  0
3                  5.25
…                …
100              100

"""

import sys

class InvalidArgumentError(ValueError): pass
class FileError(IOError): pass

def parseArg(argv):
    """Parses the command line arguments. Checks for errors and returns a tuple (school, [files, to, search])"""

    if not isinstance(argv, list): 
        """Check to make sure argv is a list"""
        raise InvalidArgumentError('Must pass a list to parseArg.')

    if(len(argv)<4):
        """All arguments must have the form ['ecdf.py', '--school', '"name_of_university"', input_file1.csv]"""
        raise InvalidArgumentError("""This program must be run with the following format: \npython ecdf.py --school “Port Chester University” file1.csv file2.csv""")
    
    if(argv[1] != "--school"):
        """This program only has one option: to aggregate according to school"""
        raise InvalidArgumentError("""This program must be run with the following format: \npython ecdf.py --school “Port Chester University” file1.csv file2.csv""")

    return (argv[2], argv[3:])





def getData(university, files):
    for this_file in files:
        try:
            f = open(this_file)
            for line in f:
                pass
        except IOError:
            error_string = "Could not open "+ str(this_file)+". Check that the path is correct."
            raise FileError (error_string) 


if __name__ == '__main__':
    school, files = parseArg(sys.argv)
    getData(school, files)
