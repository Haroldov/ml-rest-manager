CREATE TABLE IF NOT EXISTS `ml_binary_model`(
       `model_id` VARCHAR(255) NOT NULL,
       `model` BLOB NOT NULL,
       `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
	                      ON UPDATE CURRENT_TIMESTAMP,
       CONSTRAINT ml_binary_model_pk PRIMARY KEY (model_id)
);

CREATE TABLE IF NOT EXISTS `ml_metadata`(
       `model_id` VARCHAR(255) NOT NULL,
       `model_type` VARCHAR(255) NOT NULL,
       `init_params` JSON NOT NULL,
       `num_classes` INT NOT NULL,
       `num_features` INT NOT NULL,
       `num_training` INT NOT NULL,
       CONSTRAINT ml_metadata_pk PRIMARY KEY (model_id)
);
