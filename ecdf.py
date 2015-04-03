"""ECDF
Suppose you have multiple text files, each containing lines of the form:
student_id,course_name,school_name,test_date,test_score

An example valid line could look like the following (note that the files will not have headers):
9812345,"Algebra","Port Chester University",2015-03-17,75.5

Write a program to compute the empirical cumulative distribution function of the average test score of students who attended a particular school, which is specified as a parameter to the program.

An example invocation of the program would be:
python ecdf.py --school "Port Chester University" input_file1.csv input_file2.csv

The expected output from invoking such a program would be of the following form (use a single tab character to delimit field values, and display the results to standard output):

Port Chester University students

percentile    mean_test_score
1                  0
2                  0
3                  5.25
...               ...
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
        raise InvalidArgumentError("""This program must be run with the following format: \npython ecdf.py --school "Port Chester University" file1.csv file2.csv""")
    
    if(argv[1] != "--school"):
        """This program only has one option: to aggregate according to school"""
        raise InvalidArgumentError("""This program must be run with the following format: \npython ecdf.py --school "Port Chester University" file1.csv file2.csv""")

    return (argv[2], argv[3:])





def getData(university, files):

    if not isinstance(files, list): 
        """Check to make sure files is a list"""
        raise InvalidArgumentError('Format should be getData("ABC University", ["file1.csv", "file2.csv"]')

    if not isinstance(university, str): 
        """Check to make sure university is a string"""
        raise InvalidArgumentError('Format should be getData("ABC University", ["file1.csv", "file2.csv"]')
        
    if not all([isinstance(f, str) for f in files]):
        """Check to make sure that all the files are strings"""
        raise InvalidArgumentError('Format should be getData("ABC University", ["file1.csv", "file2.csv"]')

    if not all([f[-4:] == ".csv" for f in files]):
        """Check to make sure that all the files are in .csv format"""
        raise FileError('This program requires all files to have a .csv extension')

    #We will temporarily put the student test scores in a dictionary
    data = {}

    for this_file in files:
        try:
            f = open(this_file)
            error_string = "The file "+str(this_file)+" is not formatted in the correct format."

            for line in f:
                data_line = line.strip().split(",")
                
                if(len(data_line) != 5):
                    raise FileError(error_string+" Length != 5")
                try:
                    student_id = int(data_line[0])
                    score = float(data_line[4])
                except ValueError:
                    raise FileError(error_string+" student_id or score not numeric")
                """    
                if((data_line[2][0] != '"') or (data_line[2][-1] != '"')):
                    raise FileError(error_string+" The school name is not surrounded by quotes as defined in the API")"""

                school = data_line[2].strip('"')
                if(school == university):
                    try:
                        data[student_id].append(score)
                    except KeyError:
                        data[student_id] = [score]

        except FileError as e:
            f.close()
            raise(e)  
              
        except IOError:
            error_string = "Could not open "+ str(this_file)+". Check that the path is correct."
            raise FileError (error_string)

        else:
            f.close()

    if(len(data) == 0):
        raise FileError ("Did not find any data for "+university)


    #Now that we have all of the student data, we will want to get the average for each student
    output = []  
    for student in data:
        output.append(sum(data[student])/len(data[student]))

    #Finally, we will want to return the sorted data
    return sorted(output)


def makeECDF(data):
    if not isinstance(data, list): 
        """Check to make sure data is a list"""
        raise InvalidArgumentError("makeECDF only accepts lists")
    
    if sorted(data) != data:
        """Checking to make sure the data is sorted"""
        raise InvalidArgumentError("makeECDF accepts only sorted lists")

    if len(data) == 0:
        """There must be some data for us to run ECDF on"""
        raise InvalidArgumentError("The length of the data was zero. There must be at least one data point.")


    n = len(data)-1 #the negative one makes it match up with np.percentile
    out = []
    for i in range(100):
        out.append(data[int(n*i/100)])
    return out

def printECDF(school, ecdf):

    if not isinstance(ecdf, list): 
        """Check to make sure data is a list"""
        raise InvalidArgumentError("printECDF needs a list")
    
    if sorted(ecdf) != ecdf:
        """Checking to make sure the data is sorted"""
        raise InvalidArgumentError("printECDF accepts only sorted lists")

    if len(ecdf) != 100:
        """The must be some data for us to run ECDF on"""
        raise InvalidArgumentError("The length of the data was not 100.")

    if not isinstance(school, str): 
        """Check to make sure data is a list"""
        raise InvalidArgumentError("printECDF needs the name of a school")

    output = school+ " students\n\npercentile\tmean_test_score\n"
    for i in range(100):
        output = output+str(i+1)+'\t'+str(ecdf[i])+'\n'


    return output




"""


Port Chester University students

percentile    mean_test_score
1                  0
2                  0
3                  5.25
...               ...
100              100
"""
    
    

if __name__ == '__main__':
    school, files = parseArg(sys.argv)
    data = getData(school, files)
    ecdf = makeECDF(data)
    print(printECDF(school, ecdf))
