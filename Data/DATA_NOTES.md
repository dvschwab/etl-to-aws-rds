# Notes on Project Data

There are six data files for this project. The first three contain the entire data set from its journey from unprocessed data to the data that is ready to be staged.

* pokemon_initial_data.csv: the initial data set from Kaggle with no processing or changes.
* pokemon_modified_data.csv: the initial data set with a few non-printable characters removed. This is the input to remove_kanji.py.
* pokemon_ready_to_stage.dat: the output of remove_kanji.py without kanji characters. This is what should be loaded into the staging table.

The remaining three files are the data to be loaded into their respective tables using the loading scripts.

* pokemon_ability.dat
* pokemon_classification.dat
* pokemon_species.dat

All files have Linux line endings. The CSV files have comma delimiters, while the DAT files are pipe-delimited.
