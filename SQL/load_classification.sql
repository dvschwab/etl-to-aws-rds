-- Load the classification dimension table
-- This must be done prior to creating the statistics table,
-- or the classification_id FK on that table must be removed

use pokemon;
load data local infile '../Data/pokemon_classification.dat'
into table classification
	character set utf8mb4
	lines terminated by '\n'
(classification_type);
