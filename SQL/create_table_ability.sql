-- Create table to store pokemon abilities

CREATE TABLE IF NOT EXISTS abilities (
	ability_id bigint not null auto_increment unique primary key,
	ability varchar(50)
)
