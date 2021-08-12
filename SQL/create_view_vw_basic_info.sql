CREATE VIEW `pokemon`.`vw_basic_info` AS
	select `stats`.`english_name` AS `english_name`,
	`pokemon`.`classification`.`classification_type` AS `classification_type`,
	`pokemon`.`species`.`species_type` AS `species_type`,
	`stats`.`hit_points` AS `hit_points`,
	`abil`.`ability_type` AS `ability_type`,
	`stats`.`attack` AS `attack`,
	`stats`.`defense` AS `defense`,
	`stats`.`speed` AS `speed`,
	`stats`.`base_happiness` AS `base_happiness`,
	`stats`.`capture_rate` AS `capture_rate`,
	`stats`.`height_m` AS `height_m`,
	`stats`.`weight_kg` AS `weight_kg`,
	`stats`.`percentage_male` AS `percentage_male`,
	`stats`.`generation` AS `generation`,
	(case `stats`.`is_legendary`
		when 1 then 'True' 
		else 'False'
	end) AS `is_legendary`
	from ((((`pokemon`.`statistics` `stats`
	join `pokemon`.`species` on((`pokemon`.`species`.`species_id` = `stats`.`species_id`)))
	join `pokemon`.`classification` on((`pokemon`.`classification`.`classification_id` = `stats`.`classification_id`)))
	join `pokemon`.`statistics_to_abilities_xwalk` `xwalk` on((`xwalk`.`pokemon_id_FK` = `stats`.`pokemon_id`)))
	join `pokemon`.`ability` `abil` on((`abil`.`ability_id` = `xwalk`.`ability_id_FK`)))
	order by `stats`.`english_name`,`abil`.`ability_type`;
