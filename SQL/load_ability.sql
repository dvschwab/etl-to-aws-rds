-- Load the ability dimension table

use pokemon;
load data local infile '../Data/pokemon_ability.dat'
into table ability
		character set utf8mb4
		lines terminated by '\n'
(ability_type);
