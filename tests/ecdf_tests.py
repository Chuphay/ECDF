"""Unit tests for ECDF, an empirical cumulative distribution function finder. Since I am using a test-first development strategy, there will be some comments in this script that describe my thinking process as I build the package.

I have decided to have four main functions in the program: parseArg, getData, makeECDF, printECDF. ParseArg will take the arguments provided by the user and parse them to make sure that they are valid. GetData will then take those arguments and scan through the selected files for the relevant information. MakeECDF will then take that data and return the ECDF in a compact form. PrintECDF will take the ECDF provided by MakeECDF and return a string that is in the correct format."""

from ecdf.ecdf import *
import unittest

scipy_imported = False #this will check to see if I loaded ECDF from the scipy stack
try:
    import numpy as np
    from statsmodels.distributions.empirical_distribution import ECDF
    scipy_imported = True
except ImportError:
    print("Could not load statsmodels. Will not be able to test all aspects of ecdf")



class TestParseArg(unittest.TestCase):
    """I will divide my tests into two parts, first inputs that should return errors and then, secondly, inputs that should return correct output"""

    def test_wrong_type_of_argument(self):
        """testing for non-array arguments"""
        self.assertRaises(InvalidArgumentError, parseArg, "string")
        self.assertRaises(InvalidArgumentError, parseArg, True)
        self.assertRaises(InvalidArgumentError, parseArg, 3.14)

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
    """I will divide my tests into three parts, first inputs that should return errors and then, secondly, inputs that pass into getData, but then return bad data. And finally I'll check good inputs."""

    def test_wrong_type_of_arguments(self):
        """testing to make sure it only accepts a string and a list"""
        self.assertRaises(ValueError, getData, "string", "string")
        self.assertRaises(ValueError, getData, "string", 3.14)
        self.assertRaises(ValueError, getData, 3.14, "string")
        self.assertRaises(ValueError, getData, 3.14, [1,"string"])
        self.assertRaises(ValueError, getData, "string", [1,"string"])

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
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad2.csv"])
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad3.csv"])
        self.assertRaises(FileError, getData, "ABC University", ["tests/bad4.csv"])












if __name__ == '__main__':
    unittest.main()
