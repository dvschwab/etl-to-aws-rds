use pokemon;
truncate ability;
load data local infile '../Data/pokemon_ability.dat'
into table ability 
lines terminated by '\n'
(ability_type)
