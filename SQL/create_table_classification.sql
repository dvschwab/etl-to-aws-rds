-- Create the classification dimension table
-- classification_type is unique
-- classification_id is PK to classification_id PK in statistics table

CREATE TABLE IF NOT EXISTS `classification` (
  `classification_id` bigint NOT NULL AUTO_INCREMENT,
  `classification_type` varchar(100) NOT NULL,
  PRIMARY KEY (`classification_id`),
  UNIQUE KEY `classification_id` (`classification_id`),
  UNIQUE KEY `classification_type_UNIQUE` (`classification_type`)
) AUTO_INCREMENT=1;
