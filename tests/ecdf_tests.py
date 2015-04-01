"""Unit tests for ECDF, an empirical cumulative distribution function finder. Since I am using a test-first development strategy, there will be some comments in this script that describe my thinking process as I build the package.

I have decided to have four main functions in the program: parseArg, getData, makeECDF, printECDF. ParseArg will take the arguments provided by the user and parse them to make sure that they are valid. GetData will then take those arguments and scan through the selected files for the relevant information. MakeECDF will then take that data and return the ECDF in a compact form. PrintECDF will take the ECDF provided by MakeECDF and return a string that is in the correct format."""

from ecdf.ecdf import *
import unittest

scipy_imported = False #this will check to see if I loaded ECDF from the scipy stack
pandas_imported = False #this will check if Pandas was imported
try:
    import numpy as np
    from statsmodels.distributions.empirical_distribution import ECDF
    scipy_imported = True
except ImportError:
    print("Could not load statsmodels. Will not be able to test all aspects of ecdf")

try:
    import pandas as pd
except ImportError:
    print("Could not load Pandas. Will not be able to test all aspects of ecdf")




class TestParseArg(unittest.TestCase):
    """I will divide my tests into two parts. First I will check that invalid arguments raise errors. Then I will check that valid arguments return correct output"""

    def test_wrong_type_of_argument(self):
        """testing for non-array arguments"""
        self.assertRaises(InvalidArgumentError, parseArg, "string")
        self.assertRaises(InvalidArgumentError, parseArg, True)
        self.assertRaises(InvalidArgumentError, parseArg, 3.14)
        self.assertRaises(InvalidArgumentError, parseArg, None)

    def test_no_arguments(self):
        """parseArg should raise an exception if there were no arguments"""
        self.assertRaises(InvalidArgumentError, parseArg, [])

    def test_too_few_arguments(self):
        """parseArg should raise an exception if there is not enough arguments"""
        self.assertRaises(InvalidArgumentError, parseArg, ["one"])
        self.assertRaises(InvalidArgumentError, parseArg, ["one", "two"])
        self.assertRaises(InvalidArgumentError, parseArg, ["one", "two","three"])
        self.assertRaises(InvalidArgumentError, parseArg, ["ecdf.py", "--school", "Port Chester University"])

    def test_wrong_arguments(self):
        """If the arguments are not in the correct order, an Error should be thrown"""
        self.assertRaises(InvalidArgumentError, parseArg, ["ecdf.py",'file1.csv',"Port Chester University", "--school"])

    #Above were the tests for the bad inputs, now we will test the good inputs

    def test_one_file(self):
        """testing one csv file"""
        result = parseArg(["ecdf.py", "--school","Port Chester University",'file1.csv']) 
        self.assertEqual(("Port Chester University", ["file1.csv"]), result) 

    def test_multiple_files(self):
        """testing multiple csv files"""
        result = parseArg(["ecdf.py", "--school","Port Chester University",'file1.csv',"file2.csv"]) 
        self.assertEqual(("Port Chester University", ["file1.csv", "file2.csv"]), result)
        result = parseArg(["ecdf.py", "--school","Port Chester University",'file1.csv',"file2.csv", "file3.txt"]) 
        self.assertEqual(("Port Chester University", ["file1.csv", "file2.csv", "file3.txt"]), result)



class TestGetData(unittest.TestCase):
    """I will divide my tests into three parts. First I will check for arguments that should return errors. Then, I will check for bad data in the csv file itself. Finally I will check that good inputs return correct results."""

    def test_wrong_type_of_arguments(self):
        """testing to make sure it only accepts a string and a list"""
        self.assertRaises(InvalidArgumentError, getData, "string", "string")
        self.assertRaises(InvalidArgumentError, getData, "string", 3.14)
        self.assertRaises(InvalidArgumentError, getData, 3.14, "string")
        self.assertRaises(InvalidArgumentError, getData, 3.14, [1,"string"])
        self.assertRaises(InvalidArgumentError, getData, "string", [1,"string"])
        self.assertRaises(InvalidArgumentError, getData, "string", None)
        self.assertRaises(InvalidArgumentError, getData, None, ["string","string"])

    def test_file_extension(self):
        """testing to make sure it accepts only .csv files"""
        self.assertRaises(FileError, getData, "string", ["file1.csv","file2.txt"])


    def test_no_file_present(self):
        """test to make sure that the file asked for is actually found"""
        self.assertRaises(FileError, getData, "ABC University", ["file1.csv", "not_a_file.csv", "file2.csv"])

    #Now, I will check for bad data
    def test_for_correct_number_of_elements(self):
        """testing that all lines of the files have the correct number of elements"""
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad1.csv"])

    def test_for_no_quotes(self):
        """testing for quotes around the University name"""
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad2.csv"])

    def test_for_score_is_float(self):
        """test to make sure that the test score is a float"""
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad3.csv"])

    def test_for_student_id(self): 
        """testing to make sure that the student Id is an integer""" 
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad4.csv"])

    def test_for_no_school(self):
        """If the files do not contain any information about that school, we want an error"""
        self.assertRaises(FileError, getData, "XYZ University",  ['tests/file1.csv',"tests/file2.csv"]) 

    #Now, I will check that the output is correct
    def test_ABC_University(self):
        """checking over two csv files for ABC University"""
        result = getData("ABC University", ['tests/file1.csv',"tests/file2.csv"]) 
        self.assertEqual([55.0, 62.5, 83.5], result)

    def test_DEF_University(self):
        """checking over one csv file for DEF University"""
        result = getData("DEF University", ['tests/file1.csv']) 
        self.assertEqual([10.0, 35.0, 45.0], result)

    def test_one_entry(self):
        """Checking if it handles only one entry"""
        result = getData("Port Chester University", ['tests/file1.csv']) 
        self.assertEqual([75.5], result)
        

class TestMakeECDF(unittest.TestCase):
    """I will divide my tests into two parts. First I will check that invalid arguments raise errors. Then I will check that valid arguments return correct output"""

    def test_wrong_type_of_argument(self):
        """testing for non-array arguments"""
        self.assertRaises(InvalidArgumentError, makeECDF, "string")
        self.assertRaises(InvalidArgumentError, makeECDF, True)
        self.assertRaises(InvalidArgumentError, makeECDF, 3.14)
        self.assertRaises(InvalidArgumentError, makeECDF, None)

    def test_array_has_elements(self):
        """checking that it rejects []"""
        self.assertRaises(InvalidArgumentError, makeECDF, [])

    def test_array_is_sorted(self):
        """Since the input should be sorted, it should reject non-sorted data"""
        self.assertRaises(InvalidArgumentError, makeECDF, [3,2])

    def test_length_100(self):
        result = makeECDF(sorted([0.4,0.55,0.7,0.85, 1.97,3.77, -4.5, -2]))
        self.assertEqual(100, len(result))

    def test_sorted(self):
        result = makeECDF(sorted([0.4,0.55,0.7,0.85, 1.97,3.77, -4.5, -2]))
        self.assertEqual(result, sorted(result))

    def test_correct_answer(self):
        result = makeECDF(sorted([0.4,0.55,0.7,0.85, 1.97,3.77, -4.5, -2]))
        self.assertEqual([-4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77]
, result)


class TestPrintECDF(unittest.TestCase):




    def test_wrong_type_of_argument(self):
        """testing for non-array arguments"""
        self.assertRaises(InvalidArgumentError, printECDF, "string")
        self.assertRaises(InvalidArgumentError, printECDF, True)
        self.assertRaises(InvalidArgumentError, printECDF, 3.14)
        self.assertRaises(InvalidArgumentError, printECDF, None)

    def test_for_non_sorted_elements(self):
        bad_data = [3.77, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 1.97, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, 3.77, -4.5]
        self.assertRaises(InvalidArgumentError, printECDF, bad_data)

    def test_for_not_100_elements(self):
        bad_data2 = [-4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -4.5, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4]
        self.assertRaises(InvalidArgumentError, printECDF, bad_data2)


        












if __name__ == '__main__':
    unittest.main()
