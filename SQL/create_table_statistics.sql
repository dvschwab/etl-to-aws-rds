-- Create table for storing pokemon stats

CREATE TABLE IF NOT EXISTS statistics (
	pokemon_id bigint not null auto_increment unique primary key,
	english_name varchar(50) not null unique,
	classification_id bigint,
	species_id bigint,
	hit_points integer,
	attack integer,
	defense integer,
	speed integer,
	sp_attack integer,
	sp_defense integer,
	against_bug float,
	against_dark float,
	against_dragon float,
	against_electric float,
	against_fairy float,
	against_fight float,
	against_fire float,
	against_flying float,
	against_ghost float,
	against_grass float,
	against_ground float,
	against_ice float,
	against_normal float,
	against_poison float,
	against_psychic float,
	against_rock float,
	against_steel float,
	against_water float,
	base_egg_steps integer,
	base_happiness integer,
	base_total integer,
	capture_rate integer,
	experience_growth integer,
	height_m float,
	weight_kg float,
	percentage_male float,
	pokedex_number integer,
	generation integer,
	is_legendary boolean,
    
    index ndx_classification_id_FK (classification_id),
    index ndx_species_id_FK (species_id),
    
    foreign key classification_id_FK (classification_id)
    references classification (classification_id),
    
    foreign key species_id_FK (species_id)
	references species (species_id)
)