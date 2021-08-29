-- Resets the statistics and xwalk tables so they can be loaded anew

delimiter //
create procedure reset_primary_tables()
begin

start transaction;

	--Exception handler

	declare exit handler for sqlexception
		begin
			show errors;
			rollback;   
		end;
        
	start transaction;

	-- Truncate the xwalk table, then
	-- Remove the FK constraints on the xwalk table
	-- so the statistics table can be truncated

	truncate statistics_to_abilities_xwalk;
	alter table statistics_to_abilities_xwalk drop constraint statistics_to_abilities_xwalk_ability_id_FK;
	alter table statistics_to_abilities_xwalk drop constraint statistics_to_abilities_xwalk_pokemon_id_FK;
    
    -- Truncate statistics table
	-- This also resets the auto_increment counter

	truncate statistics;

	-- Add the contraints back

	alter table statistics_to_abilities_xwalk
	add constraint statistics_to_abilities_xwalk_ability_id_FK
	foreign key ndx_ability_id_FK (ability_id_FK)
	references ability (ability_id);

	alter table statistics_to_abilities_xwalk
	add constraint statistics_to_abilities_xwalk_pokemon_id_FK
	foreign key ndx_pokemon_id_FK (pokemon_id_FK)
	references statistics (pokemon_id);
    
   commit;
end
delimiter ;