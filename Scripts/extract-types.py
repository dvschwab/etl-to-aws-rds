# Extracts a list of pokemon types from the data file
# so they can be normalized in the db.
# DVS 7/11/2021

import csv

# Position of *type* field in data file
TYPE_FIELD = 35

input_file = "Data\\pokemon_filtered.dat"
output_file = "Data\\pokemon_types.dat"

def extract_types(file_reader):
    """
        Returns a sorted list of all pokemon types
        in the file_reader
    """

    type_list = []

    # Process each file row
    for row in file_reader:
       type_list.append(row[TYPE_FIELD])

    # Make a new list with each unique type
    # list(set(*)) removes dups (set) and returns a list
    unique_type_list = list(set(type_list))
    unique_type_list.sort()

    return unique_type_list   

if __name__ == '__main__':
    
    f = open(input_file, 'rt')
    csv_reader = csv.reader(f, delimiter = '|')

    types = extract_types(csv_reader)
    f.close()

    with open(output_file, 'wt') as f:
        for type in types[0:-1]:
            f.write(type + '\n')
        f.write(types[-1])