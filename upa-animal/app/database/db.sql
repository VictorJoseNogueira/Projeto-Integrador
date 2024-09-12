-- Criação da tabela `tutor`
CREATE TABLE `tutor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `cpf` varchar(14) NOT NULL,
  `tel` varchar(20) NOT NULL,
  `endereco` varchar(255) NOT NULL,
  `deleted` tinyint(1) DEFAULT '0',
  `deleted_by` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `cpf_UNIQUE` (`cpf`)
) ENGINE=InnoDB AUTO_INCREMENT=164 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `animal`
CREATE TABLE `animal` (
  `animal_id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `peso_aproximado` decimal(5,2) NOT NULL,
  `idade_aproximado` int NOT NULL,
  `id_tutor` int NOT NULL,
  `especie` varchar(255) NOT NULL,
  `sexo` enum('macho','femea') NOT NULL,
  PRIMARY KEY (`animal_id`),
  KEY `fk_tutor_id` (`id_tutor`),
  CONSTRAINT `fk_tutor_id` FOREIGN KEY (`id_tutor`) REFERENCES `tutor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `consulta`
CREATE TABLE `consulta` (
  `id_consulta` int NOT NULL AUTO_INCREMENT,
  `id_animal` int NOT NULL,
  `id_tutor` int NOT NULL,
  `veterinario` int NOT NULL,
  `sintomas` text NOT NULL,
  `procedimento` text NOT NULL,
  `medicacao` text,
  `observacao` text,
  `data` datetime NOT NULL,
  PRIMARY KEY (`id_consulta`),
  KEY `fk_animal_id` (`id_animal`),
  KEY `fk_consulta_tutor_id` (`id_tutor`),
  KEY `fk_veterinario_id` (`veterinario`),
  CONSTRAINT `fk_animal_id` FOREIGN KEY (`id_animal`) REFERENCES `animal` (`animal_id`),
  CONSTRAINT `fk_consulta_tutor_id` FOREIGN KEY (`id_tutor`) REFERENCES `tutor` (`id`),
  CONSTRAINT `fk_veterinario_id` FOREIGN KEY (`veterinario`) REFERENCES `administradores` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `administradores`
CREATE TABLE `administradores` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `senha` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Criação da tabela `tutor_animal`
CREATE TABLE `tutor_animal` (
  `id` int NOT NULL AUTO_INCREMENT,
  `tutor_id` int NOT NULL,
  `animal_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tutor_id` (`tutor_id`),
  KEY `animal_id` (`animal_id`),
  CONSTRAINT `tutor_animal_ibfk_1` FOREIGN KEY (`tutor_id`) REFERENCES `tutor` (`id`),
  CONSTRAINT `tutor_animal_ibfk_2` FOREIGN KEY (`animal_id`) REFERENCES `animal` (`animal_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
