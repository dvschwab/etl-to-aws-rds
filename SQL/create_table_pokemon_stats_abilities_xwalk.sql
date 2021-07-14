-- Create crosswalk table to relate each pokemon to their abilities
-- This is many-to-many, as each pokemon can have multiple abilities
-- and each ability may belong to several different pokemon

CREATE TABLE IF NOT EXISTS statistics_to_abilities_xwalk (
	pokemon_id_FK bigint not null,
	ability_id_FK bigint not null,

	index (pokemon_id_FK),
	index (ability_id_FK),

	constraint statistics_to_abilities_xwalk_pokemon_id_FK
    foreign key (pokemon_id_FK)
	references statistics (pokemon_id)
	on update cascade on delete cascade,

	constraint statistics_to_abilities_xwalk_ability_id_FK
	foreign key (ability_id_FK)
	references abilities (ability_id)
	on update cascade on delete restrict
)