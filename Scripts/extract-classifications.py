# Extracts a list of pokemon classifications from the data file
# so they can be normalized in the db.
# DVS 7/20/2021

import csv

# Position of *classification* field in data file
CLASSIFICATION_FIELD = 24

input_file = "Data\\pokemon_filtered.dat"
output_file = "Data\\pokemon_classifications.dat"

def extract_classifications(file_reader):
    """
        Returns a sorted list of all pokemon classifications
        in the file_reader
    """

    classification_list = []

    # Process each file row
    for row in file_reader:
       classification_list.append(row[CLASSIFICATION_FIELD])

    # Make a new list with each unique type
    # list(set(*)) removes dups (set) and returns a list
    unique_classification_list = list(set(classification_list))
    unique_classification_list.sort()

    return unique_classification_list   

if __name__ == '__main__':
    
    f = open(input_file, 'rt')
    csv_reader = csv.reader(f, delimiter = '|')

    classifications = extract_classifications(csv_reader)
    f.close()

    with open(output_file, 'wt') as f:
        for pokemon_class in classifications[0:-1]:
            f.write(pokemon_class + '\n')
        f.write(classifications[-1])