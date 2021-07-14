# Short script to extract a list of unique pokemon abilities
# and save them to CSV for later import into MySQL
# Needed because the abilities field in main data file
# stores them as variable-length arrays
# DVS 7/2/2021

import csv

# Position of *ability* field in data file
ABILITY_FIELD = 0

input_file = "Data\\pokemon-filtered.dat"
output_file = "Data\\pokemon-abilities.dat"

def extract_abilities(file_reader):
    """
        Returns a sorted list of all pokemon abilities
        in the file_reader
    """

    ability_list = []

    # Process each file row
    for row in file_reader:
        # Get the *ability* field and remove brackets
        row_strip = row[ABILITY_FIELD].strip("[]")

        # Split the field into single-string elements
        for ability in row_strip.split(","):
            # Remove unneeded chars and append
            ability_strip = ability.strip(" '")
            ability_list.append(ability_strip)

    # Make a new list with each unique ability
    # list(set(*)) removes dups (set) and returns a list
    unique_ability_list = list(set(ability_list))
    unique_ability_list.sort()

    return unique_ability_list   

if __name__ == '__main__':
    
    f = open(input_file, 'rt')
    csv_reader = csv.reader(f, delimiter = '|')

    abilities = extract_abilities(csv_reader)
    f.close()

    with open(output_file, 'wt') as f:
        for ability in abilities[0:-1]:
            f.write(ability + '\n')
        f.write(abilities[-1])