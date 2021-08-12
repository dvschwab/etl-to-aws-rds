-- Create crosswalk table to relate each pokemon to its abilities
-- This is many-to-many, as each pokemon can have multiple abilities
-- and each ability may belong to several different pokemon
-- pokemon_id_FK is FK to pokemon_id PK in the statistics table
-- ability_id_FK is FK to ability_id PK in the ability table
-- composite key (pokemon_id_FK, ability_id_FK) is a PK

CREATE TABLE IF NOT EXISTS `statistics_to_abilities_xwalk` (
  `pokemon_id_FK` bigint NOT NULL,
  `ability_id_FK` bigint NOT NULL,
  KEY `pokemon_id_FK` (`pokemon_id_FK`),
  KEY `ability_id_FK` (`ability_id_FK`),
  PRIMARY KEY (pokemon_id_FK, ability_id_FK)
  CONSTRAINT `statistics_to_abilities_xwalk_ability_id_FK` FOREIGN KEY (`ability_id_FK`) REFERENCES `ability` (`ability_id`),
  CONSTRAINT `statistics_to_abilities_xwalk_pokemon_id_FK` FOREIGN KEY (`pokemon_id_FK`) REFERENCES `statistics` (`pokemon_id`)
);