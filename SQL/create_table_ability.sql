-- Create abilities dimension table
-- ability_type is unique

CREATE TABLE IF NOT EXISTS abilities (
	ability_id bigint not null auto_increment,
	ability varchar(50) not null,
	primary key (ability_id),
	unique key ability_id (ability_id),
	unique key ability_UNIQUE (ability_type)
) auto_increment=0;
