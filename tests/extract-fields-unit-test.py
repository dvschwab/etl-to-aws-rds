# Runs the unit tests for the extract-field module
# DVS 8/28/2021

import csv
import unittest as ut
from unittest.case import TestCase
from data_extract.extract_field import extract_delimited_field, extract_field_from_file, write_field_to_file

class TestFileDelimiters(TestCase):

    # Tests whether the function can extract a field from a file
    # using one of the supported delimiters

    def test_csv(self):
        with open('tests/input/pokemon_test_data_input_csv.dat') as input:
            csv_reader = csv.reader(input, delimiter = ',')
            input_field = extract_delimited_field(csv_reader, 0)
        with open('tests/input/pokemon_test_data_output_1.csv') as output:
            csv_reader = csv.reader(output, delimiter = ',')
            output_field = extract_delimited_field(csv_reader, 0)
        self.assertEqual(input_field, output_field)

    def test_pipe(self):
        with open('tests/input/pokemon_test_data_input_pipe.dat') as input:
            csv_reader = csv.reader(input, delimiter = '|')
            input_field = extract_delimited_field(csv_reader, 0)
        with open('tests/input/pokemon_test_data_output_1.csv') as output:
            csv_reader = csv.reader(output, delimiter = ',')
            output_field = extract_delimited_field(csv_reader, 0)
        self.assertEqual(input_field, output_field)

    def test_semicolon(self):
        with open('tests/input/pokemon_test_data_input_semicolon.dat') as input:
            csv_reader = csv.reader(input, delimiter = ';')
            input_field = extract_delimited_field(csv_reader, 0)
        with open('tests/input/pokemon_test_data_output_1.csv') as output:
            csv_reader = csv.reader(output, delimiter = ',')
            output_field = extract_delimited_field(csv_reader, 0)
        self.assertEqual(input_field, output_field)

class TestPosition(TestCase):

    # Tests whether the function can handle illegal position arguments

    def test_position_not_integer(self):
        with open('tests/input/pokemon_test_data_input_csv.dat') as input:
            csv_reader = csv.reader(input, delimiter = ',')
            with self.assertRaises(TypeError):
                extract_delimited_field(csv_reader, 0.5)

    def test_position_negative(self):
        with open('tests/input/pokemon_test_data_input_csv.dat') as input:
            csv_reader = csv.reader(input, delimiter = ',')
            with self.assertRaises(ValueError):
                extract_delimited_field(csv_reader, -1)

    def test_position_overflow(self):
        with open('tests/input/pokemon_test_data_input_csv.dat') as input:
            csv_reader = csv.reader(input, delimiter = ',')
            with self.assertRaises(IndexError):
                extract_delimited_field(csv_reader, 3) 

class TestFileHandling(TestCase):

    # Tests whether the function can handle invalid file names

    def test_file_input_error(self):
        with self.assertRaises(IOError):
            extract_field_from_file('not/a/real/file', 1)

    def test_file_output_error(self):
        field = []
        with self.assertRaises(IOError):
            write_field_to_file('not/a/real/file', field)

class TestSorting(TestCase):

    # Tests whether the function sorts correctly when sorted=True

    def test_sorted(self):
        input_file = 'tests/input/pokemon_test_data_input_csv.dat'
        output_field = extract_field_from_file(input_file, 2, sorted=True)
        with open('tests/input/pokemon_test_data_output_3_sorted.csv', 'rt') as test_file:
            sorted_field = [line.rstrip() for line in test_file]
        self.assertEqual(output_field, sorted_field)

if __name__ == '__main__':
    ut.main()
