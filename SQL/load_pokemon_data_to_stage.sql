-- Load pokemon data into the staging table

start transaction;

	use pokemon;
	truncate stage;
	load data local infile 'C:\\Users\\dvschwab\\Documents\\Programming\\Python3\\pokemon-analysis-and-classification\\Data\\pokemon_filtered.dat'
	into table stage
		fields terminated by '|'
		optionally enclosed by '"'
	(abilities, against_bug, against_dark, against_dragon, against_electric, against_fairy, against_fight, against_fire, against_flying, against_ghost,
	against_grass, against_ground, against_ice, against_normal, against_poison, against_psychic, against_rock, against_steel, against_water,
	attack, base_egg_steps, base_happiness, base_total, capture_rate, classification, defense, experience_growth, height_m, hp, english_name,
	percentage_male, pokedex_number, sp_attack, sp_defense, speed, type1, type2, weight_kg, generation, is_legendary);

commit;