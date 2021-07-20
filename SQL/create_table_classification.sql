USE pokemon;
CREATE TABLE `classification` (
  `classification_id` bigint NOT NULL AUTO_INCREMENT,
  `classification` varchar(100) NOT NULL,
  PRIMARY KEY (`classification_id`),
  UNIQUE KEY `classification_id` (`classification_id`),
  UNIQUE KEY `classification_UNIQUE` (`classification`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
