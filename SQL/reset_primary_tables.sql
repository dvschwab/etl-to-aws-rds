-- Resets the statistics and xwalk tables so they can be loaded anew

start transaction;

	use pokemon;

	-- Truncate the xwalk table, then
	-- Remove the FK constraints on the xwalk table
	-- so the statistics table can be truncated

	truncate statistics_to_abilities_xwalk;
	alter table statistics_to_abilities_xwalk drop constraint statistics_to_abilities_xwalk_ability_id_FK;
	alter table statistics_to_abilities_xwalk drop constraint statistics_to_abilities_xwalk_pokemon_id_FK;
    
    -- Drop FK constraint to statistics table and truncate the species table
    
	alter table statistics drop constraint species_id_FK;
    truncate species;
    
	-- Truncate statistics table
	-- This also resets the auto_increment counter

	truncate statistics;

	-- Add the contraints back

	alter table statistics_to_abilities_xwalk
	add constraint statistics_to_abilities_xwalk_ability_id_FK
	foreign key ndx_ability_id_FK (ability_id_FK)
	references abilities (ability_id);

	alter table statistics_to_abilities_xwalk
	add constraint statistics_to_abilities_xwalk_pokemon_id_FK
	foreign key ndx_pokemon_id_FK (pokemon_id_FK)
	references statistics (pokemon_id);
    
    alter table statistics
    add constraint species_id_FK
    foreign key ndx_species_id_FK (species)
    references species (species_id);

commit;