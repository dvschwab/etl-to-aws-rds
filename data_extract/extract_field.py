# Extracts a list of unique values for a given field in a delimited file
# Optionally sorts the list
# Intended usage is to extract dimension fields from a data file
# so they can be loaded into a database table
# DVS 7/27/2021

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

if __name__ == '__main__':
    
    # Parse CLI args
    
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="The file to be processed")
    parser.add_argument("output_file", help="The output file")
    parser.add_argument("field_position", type=int, help="The numeric position of the field to be extracted (zero-based)")
    parser.add_argument("-d", "--delimiter", choices=['tab', 'pipe', 'semi-colon'], help="The file delimiter of the input file")
    parser.add_argument("-s", "--sorted", action = "store_true", help="Whether the output file should be sorted in ascendant order.")
    args = parser.parse_args()

    # Set the delimiter or use the default
    if not args.delimiter:
        delimiter = ','
    elif args.delimiter == 'tab':
        delimiter = '\t'
    elif args.delimiter == 'pipe':
        delimiter = '|'
    elif args.delimiter == 'semi-colon':
        delimiter = ';'
    else:
        print("Delimiter must be one of 'tab', 'pipe', or 'semi-colon'. This should have been caught by argparse: something may be wrong with that part of the code.")
        exit()

    # Open the file and extract the field
    try:
        with open(args.input_file, 'rt') as f:
            csv_reader = csv.reader(f, delimiter = delimiter)
            field = extract_delimited_field(csv_reader, args.field_position)
    except OSError:
        print(f'There was an error in opening or reading the file {args.input_file}. Make sure the file exists and is not corrupt.')
    except:
        print('There was an error while extracting the field values. The program has terminated.')

    # Sort field if user desires
    if args.sorted:
        field.sort()

    # Writer output file
    # Wonky use of two f.write() is to remove trailing newline
    try:
        with open(args.output_file, 'wt') as f:
            for value in field[0:-1]:
                f.write(value + '\n')
            f.write(field[-1])
    except IOError:
        print(f'There was an error writing data to the file {args.output_file}. Make sure the filename is valid and the program can write to the output folder.')