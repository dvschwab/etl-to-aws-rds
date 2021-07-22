-- Load the classification table
-- Requires temporarily removing the FK constraint to this table
-- from the statistics table

use pokemon;

-- Remove FK constraint to classification_id from statistics table

alter table statistics drop constraint classification_id_FK;

-- Truncate and load

truncate classification;
load data local infile 'C:\\Users\\dvschwab\\Documents\\Programming\\Python3\\pokemon-analysis-and-classification\\Data\\pokemon_classifications.dat'
into table classification
lines terminated by '\n'
(classification_type);

-- Add constraint back to statistics table

alter table statistics
add constraint classification_id_FK
foreign key ndx_classification_id_FK (classification)
references classification (classification_id);