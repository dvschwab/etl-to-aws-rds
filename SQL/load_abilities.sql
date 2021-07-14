use pokemon;
truncate abilities;
load data local infile 'C:\\Users\\dvschwab\\Documents\\Programming\\Python3\\pokemon-analysis-and-classification\\Data\\pokemon-abilities.dat'
into table abilities
(ability)