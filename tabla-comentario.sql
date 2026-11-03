CREATE TABLE IF NOT EXISTS `tarea2`.`comentario` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(80) NOT NULL,
  `texto` VARCHAR(300) NOT NULL,
  `fecha` TIMESTAMP NOT NULL,
  `avistamiento_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_comentario_avistamiento1_idx` (`avistamiento_id` ASC),
  CONSTRAINT `fk_comentario_avistamiento1`
    FOREIGN KEY (`avistamiento_id`)
    REFERENCES `tarea2`.`avistamiento` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
