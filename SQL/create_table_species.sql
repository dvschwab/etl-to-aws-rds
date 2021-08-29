-- Creates the species dimension table
-- species_type is unique
-- species_id is PK to the species_id FK in the statistics table

create table if not exists species (
	species_id bigint not null auto_increment,
    species_type varchar(50),
	primary key species_id,
	unique key species_id (species_id),
	unique species_type_UNIQUE (species_type)
) auto_increment=1;
