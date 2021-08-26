# Extracts a list of unique values for a given field in a delimited file
# Optionally sorts the list
# Intended to be run as a script to extract dimension fields from a data file
# so they can be loaded into a database table, but the extract_delimited_filed()
# function is general enough to have other uses
# DVS 8/26/2021

import csv
import argparse

def extract_delimited_field(file_reader, position):
    """
        Returns a list of unique values from a delimited file for the field
        at numeric position *position* (zero-based). Assumes the file has no header;
        if it does, the header will be returned as the first element of the list.

        :param file_reader: a reader or reader like oject, typically csv.reader
        :param position: the position of the field to extract (zero-based)
        :returns: a list of unique values for that field
    """

    # Verify position agument is an integer
    if not isinstance(position, int):
        print(f'The position argument {position} is not an intger')
        raise TypeError

    # Make sure position is not negative
    if position < 0:
        raise ValueError

    # Process each file row
    try:
        field_list = [row[position] for row in file_reader]
    except IndexError:
        print(f'The specified position {position} is more than the number of fields in the file')
        raise

    # Make a new list with each unique field
    # list(set(*)) removes dups (set) and returns a list
    unique_field = list(set(field_list))

    return unique_field

def parse_cli_args():
    """
        Parses the CLI args if file is ran as a script.

        :params: None
        :returns: the populated namespace as an argparse.Namespace object
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The file to be processed")
    parser.add_argument("output_file", help="The output file")
    parser.add_argument("field_position", type=int, help="The numeric position of the field to be extracted (zero-based)")
    parser.add_argument("-d", "--delimiter", choices=['comma', 'tab', 'pipe', 'semi-colon'], help="The file delimiter of the input file")
    parser.add_argument("-s", "--sorted", action = "store_true", help="Whether the output file should be sorted in ascending order.")

    return parser.parse_args()

def extract_field_from_file(input_file, position, delimiter = ',', sorted = False):
    """
        Extracts the field at a given position from a delimited file, returning a List of unique values. Optionally sorts the field.

        :param input_file: the file containing the field to be extracted; assumed to be a delimited file using one of the supported delimiters.
        :param position: the position of the field to extract (zero-based)
        :param delimiter: the file delimiter, defaulting to comma
        :param sorted: whether the field should be sorted, defaulting to False
        :returns: a List containing the unique values of the field (optionally sorted)
    """

    # Open the file and extract the field
    try:
        with open(input_file, 'rt') as f:
            csv_reader = csv.reader(f, delimiter = delimiter)
            field = extract_delimited_field(csv_reader, position)
    except IOError:
        print(f'There was an error in opening or reading the file {input_file}. Make sure the file exists and is not corrupt.')
        raise

    # Sort field if user desires
    if sorted:
        field.sort()

    return field

def write_field_to_file(output_file, field):
    """
        Writes the specified field (a List) to the specified file with rows terminated by newlines (here, '\n'). Does NOT add a trailing newline. Will overwrite any existing file without warning.

        :param output_file: the file to write
        :param field: the field to write (any single-dimension List-like object)
        :returns: nothing
    """

    # Write output file
    # Wonky use of two f.write() is to remove trailing newline
    try:
        with open(output_file, 'wt') as f:
            for value in field[0:-1]:
                f.write(value + '\n')
            f.write(field[-1])
    except IOError:
        print(f'There was an error writing data to the file {output_file}. Make sure the filename is valid and the program can write to the output folder.')
        raise

def assign_delimiter_from_name(delimiter_name):
    """
        Returns the delimiter corresponding to the specified argument. Raises ValueError if argument is not a supported delimiter type.
        
        :param delimiter_name: the name corresponding to the delimiter to be selected. Must be one of 'comma', 'tab', 'pipe', or 'semi-colon'.
        :returns: the delimiter value (i.e. ',', '\t', '|', or ';')
    """

    # Set the delimiter
    # Allows 'comma' to be explicitly specified for users who want to do that
    
    if delimiter_name == 'comma':
        delimiter = ','
    elif delimiter_name == 'tab':
        delimiter = '\t'
    elif delimiter_name == 'pipe':
        delimiter = '|'
    elif delimiter_name == 'semi-colon':
        delimiter = ';'
    else:
        print("Delimiter must be one of 'comma', 'tab', 'pipe', or 'semi-colon'. This should have been caught by argparse: something may be wrong with that part of the code.")
        raise ValueError
    
    return delimiter

if __name__ == '__main__':

    # Parse CLI args
    args = parse_cli_args()

    # Assign delimiter (if specified) or set to comma
    if not args.delimiter:
        delimiter = ','
    else:
        delimiter = assign_delimiter_from_name(args.delimiter)
    
    # Extract field
    field = extract_field_from_file(args.input_file, args.field_position, delimiter, args.sorted)

    # Write field to file
    write_field_to_file(args.output_file, field)