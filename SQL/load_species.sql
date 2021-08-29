-- Load the species dimension table
-- This must be done prior to creating the statistics table,
-- or else the species_id FK on that table must be removed

use pokemon;

load data local infile '../Data/pokemon_species.dat'
into table species
	character set utf8mb4
	lines terminated by '\n'
(species_type);