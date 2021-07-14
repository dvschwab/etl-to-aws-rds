-- Creates the species table, which stores the types of pokemon
-- species_id is FK to the species field in the statistics table

use pokemon;
create table if not exists species (
	species_id bigint not null auto_increment unique primary key,
    species_type varchar(50)
);
