-- Load the species table
-- Requires temporarily removing the FK constraint to this table
-- from the statistics table

use pokemon;

-- Remove FK constraint to species_id from statistics table

alter table statistics drop constraint species_id_FK;

-- Truncate and load

truncate species;
load data local infile 'C:\\Users\\dvschwab\\Documents\\Programming\\Python3\\pokemon-analysis-and-classification\\Data\\pokemon_types.dat'
into table species
lines terminated by '\n'
(species_type);

-- Add constraint back to statistics table

alter table statistics
add constraint species_id_FK
foreign key ndx_species_id_FK (species_id)
references species (species_id);