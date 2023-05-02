# ************************************************************
# Sequel Pro SQL dump
# Version 4541
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Hôte: 127.0.0.1 (MySQL 5.5.5-10.4.21-MariaDB)
# Base de données: legafrik
# Temps de génération: 2023-04-12 10:56:07 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Affichage de la table admins
# ------------------------------------------------------------

DROP TABLE IF EXISTS `admins`;

CREATE TABLE `admins` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(225) NOT NULL,
  `email` varchar(225) NOT NULL,
  `password` text NOT NULL,
  `role_id` int(11) DEFAULT NULL,
  `profile_url` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  `pays_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `role_id` (`role_id`),
  KEY `admins_ibfk_2` (`pays_id`),
  CONSTRAINT `admins_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`),
  CONSTRAINT `admins_ibfk_2` FOREIGN KEY (`pays_id`) REFERENCES `pays` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `admins` WRITE;
/*!40000 ALTER TABLE `admins` DISABLE KEYS */;

INSERT INTO `admins` (`id`, `username`, `email`, `password`, `role_id`, `profile_url`, `created_at`, `updated_at`, `deleted_at`, `pays_id`)
VALUES
	(1,'Admin Super','admin@legafrik.com','$5$rounds=535000$GboH7Jn.gaookSCp$ob5Kb3.uBzuYCqEh.LSnRwE1kro7bEpPqTegwPk8ar2',1,'','2022-11-24 10:11:27','2023-03-28 12:52:01',NULL,1),
	(7,'admin 6','admin3@maissl.com','$5$rounds=535000$UE5unDxLjMSHu7ll$RFqwPhEV.HT7gui6GD7qRVCAedfYW9.S1zqEjj3NzWA',2,'','2022-12-22 11:14:58','2022-12-22 11:14:58',NULL,NULL),
	(8,'admin 2','admin2@mail.com','$5$rounds=535000$J/wSHibrTdSJJtTR$Xl/pQREDsHUN.w1tHUehIgNvmQ43BVqkcZBejzXTIh.',3,'','2023-03-22 11:38:47','2023-03-22 11:40:10',NULL,2),
	(9,'Veh Nick Goueu','vehnickgoueu+trapeze@gmail.com','$5$rounds=535000$a0vpAU5BM2aaBqmg$TsRxk5V679sZcUOL9zvmojYbFKKNMI/bGNuuGz01IPB',3,NULL,'2023-03-27 17:41:28','2023-03-27 17:41:28',NULL,NULL),
	(10,'Nick Goueu Veh','vehnickgoueu+bgr@gmail.com','$5$rounds=535000$MeAubqF0yQkJuAI6$3YKl61nAoHnK/cKzvT9qqlOd8Y8obQxjkDewFLKGXi2',3,'','2023-03-27 18:34:33','2023-03-28 12:51:42',NULL,2),
	(11,'Veh Nick Admin test ci','vehnickgoueu+adminci@gmail.com','$5$rounds=535000$cuWKYDR3oMlxZqyy$ki1Usp0/hi6CIKawJ6QjPTwbXQ5Xt33kY/u1h18hsC6',4,NULL,'2023-03-30 15:02:27','2023-03-30 15:02:27',NULL,1),
	(12,'Veh Nick bloxer','vehnickgoueu+adminbn@gmail.com','$5$rounds=535000$9/r/Es8RD0/JDbXC$Q0xamNHQROSpCZwczRBS/9cfpLlRE1/1pwUl12HfBJ/',4,NULL,'2023-03-30 15:56:20','2023-03-30 15:56:20',NULL,4),
	(13,'Morroco Admin test maroc','vehnickgoueu+testmorroco@gmail.com','$5$rounds=535000$.P/9HLENexqxLWP0$71tdDkW3h.6UTJWUyfqvXjhC9NXyBOCtvooUwavfhN2',4,NULL,'2023-03-30 17:09:27','2023-03-30 17:09:27',NULL,6),
	(14,'Veh Nick Test members','vehnickgoueu+adminbf@gmail.com','$5$rounds=535000$qahE1nt35rd4HZEl$h./.fRtmNWtXJjDa6NAIz3WzJxaIg5G0Dd0HrF5tsA9',4,NULL,'2023-03-30 17:18:24','2023-03-30 17:18:24',NULL,3),
	(15,'Senegal Admin Senegal','vehnickgoueu+adminsn@gmail.com','$5$rounds=535000$rhsAWacXWtz7LG.3$UtrWigLpBEeDr2J.memKhjFv4Z0y43YWjQWOdIsElq9',4,NULL,'2023-03-30 17:28:50','2023-03-30 17:28:50',NULL,2),
	(16,'Alexandre  N\'guessan','alex@legafrik.com','$5$rounds=535000$pUNPQ0qt3FkYgfmQ$AXAEumDXKxbPg4iSllI0KX1R5sepXT9kbVNoVV7k701',1,NULL,'2023-04-06 13:55:47','2023-04-06 13:55:47',NULL,1),
	(17,'Ingrid Lolou','Ingrid@legafrik.com','$5$rounds=535000$NrPHeq6QYQLK2O2Q$XZv9EshDvwCjdhStiBdP.lCyOEu3oCoLkJXq6NS8L13',1,NULL,'2023-04-06 13:56:13','2023-04-06 13:56:13',NULL,1),
	(18,'Audrey Brou','audrey@legafrik.com','$5$rounds=535000$HKLEJ5djX77Gpx45$lGDbXUZSXb.WBEcpUyOCp6SxveSoIIKmC1nqLMq1D66',1,NULL,'2023-04-06 13:57:02','2023-04-06 13:57:02',NULL,1),
	(19,'Awa Kone','awa@legafrik.com','$5$rounds=535000$68BomEu1.Rw..kGP$QrGvIOdoDjTmg13H7r0E5T/f5PSZj2wClCJ6.Wxc3L.',1,NULL,'2023-04-06 13:57:43','2023-04-06 13:57:43',NULL,1);

/*!40000 ALTER TABLE `admins` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table article_categorie_articles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `article_categorie_articles`;

CREATE TABLE `article_categorie_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `article_id` int(11) DEFAULT NULL,
  `categorie_article_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `article_id` (`article_id`),
  KEY `categorie_article_id` (`categorie_article_id`),
  CONSTRAINT `article_categorie_articles_ibfk_1` FOREIGN KEY (`article_id`) REFERENCES `articles` (`id`),
  CONSTRAINT `article_categorie_articles_ibfk_2` FOREIGN KEY (`categorie_article_id`) REFERENCES `categorie_articles` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `article_categorie_articles` WRITE;
/*!40000 ALTER TABLE `article_categorie_articles` DISABLE KEYS */;

INSERT INTO `article_categorie_articles` (`id`, `article_id`, `categorie_article_id`, `created_at`, `updated_at`, `deleted_at`)
VALUES
	(1,1,1,'2023-04-06 18:24:56','2023-04-06 18:24:56',NULL),
	(2,2,1,'2023-04-06 19:23:15','2023-04-06 19:23:15',NULL),
	(3,3,1,'2023-04-07 12:13:50','2023-04-07 12:13:50',NULL);

/*!40000 ALTER TABLE `article_categorie_articles` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table articles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `articles`;

CREATE TABLE `articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nom_auteur` varchar(225) DEFAULT NULL,
  `fonction_auteur` varchar(225) DEFAULT NULL,
  `photo_auteur` varchar(225) DEFAULT NULL,
  `image_article` varchar(225) DEFAULT NULL,
  `titre_article` varchar(225) DEFAULT NULL,
  `url_article` varchar(225) DEFAULT NULL,
  `resume_article` text DEFAULT NULL,
  `is_status` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  `duree_article` varchar(225) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `articles` WRITE;
/*!40000 ALTER TABLE `articles` DISABLE KEYS */;

INSERT INTO `articles` (`id`, `nom_auteur`, `fonction_auteur`, `photo_auteur`, `image_article`, `titre_article`, `url_article`, `resume_article`, `is_status`, `created_at`, `updated_at`, `deleted_at`, `duree_article`)
VALUES
	(1,'DJAMA MED','Ancien juriste','https://mouvementdux.com/wp-content/uploads/2019/08/bonhomme.png','https://www.publicdomainpictures.net/pictures/320000/nahled/background-image.png','Chat GPT-4 & Legafrik','https://www.legafrik.ci/','Ceci est le résumé de l\'article sur Chat GPT-4 & Legafrik.',1,'2023-04-06 17:59:58','2023-04-06 17:59:58',NULL,NULL),
	(2,'DJAMA MED','Ancien juriste','https://mouvementdux.com/wp-content/uploads/2019/08/bonhomme.png','https://www.publicdomainpictures.net/pictures/320000/nahled/background-image.png','Chat GPT-4 & Legafrik','https://www.legafrik.ci/','Ceci est le résumé de l\'article sur Chat GPT-4 & Legafrik.',1,'2023-04-06 18:10:50','2023-04-06 18:10:50',NULL,NULL),
	(3,'DJAMA MED','Ancien juriste','https://mouvementdux.com/wp-content/uploads/2019/08/bonhomme.png','https://www.publicdomainpictures.net/pictures/320000/nahled/background-image.png','Chat GPT-4 & Legafrik','https://www.legafrik.ci/','Ceci est le résumé de l\'article sur Chat GPT-4 & Legafrik.',1,'2023-04-06 18:21:22','2023-04-06 18:21:22',NULL,NULL);

/*!40000 ALTER TABLE `articles` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table attributions
# ------------------------------------------------------------

DROP TABLE IF EXISTS `attributions`;

CREATE TABLE `attributions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `commercial_id` int(11) DEFAULT NULL,
  `juriste_id` int(11) DEFAULT NULL,
  `formaliste_id` int(11) DEFAULT NULL,
  `demande_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `demande_id` (`demande_id`),
  CONSTRAINT `attributions_ibfk_1` FOREIGN KEY (`demande_id`) REFERENCES `demandes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



# Affichage de la table categorie_articles
# ------------------------------------------------------------

DROP TABLE IF EXISTS `categorie_articles`;

CREATE TABLE `categorie_articles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelle` varchar(225) DEFAULT NULL,
  `description` varchar(225) DEFAULT NULL,
  `is_status` tinyint(1) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `categorie_articles` WRITE;
/*!40000 ALTER TABLE `categorie_articles` DISABLE KEYS */;

INSERT INTO `categorie_articles` (`id`, `libelle`, `description`, `is_status`, `created_at`, `updated_at`, `deleted_at`)
VALUES
	(1,'Indefini','Article indéfini',1,'2023-04-06 17:28:21','2023-04-06 17:28:21',NULL);

/*!40000 ALTER TABLE `categorie_articles` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table categorie_users
# ------------------------------------------------------------

DROP TABLE IF EXISTS `categorie_users`;

CREATE TABLE `categorie_users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `libelle` varchar(225) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `libelle` (`libelle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `categorie_users` WRITE;
/*!40000 ALTER TABLE `categorie_users` DISABLE KEYS */;

INSERT INTO `categorie_users` (`id`, `libelle`, `created_at`, `updated_at`, `deleted_at`)
VALUES
	(1,'nouvelle cat','2022-11-22 10:50:57','2022-11-22 10:50:57',NULL),
	(2,'cat-user-2 update','2022-11-22 11:00:29','2022-11-22 14:12:12','2022-11-22 14:12:12'),
	(3,'cat-user-2','2022-11-22 11:05:10','2022-11-22 11:05:10',NULL),
	(4,'cat-user-to-delete','2022-11-22 11:10:35','2022-11-22 11:14:36','2022-11-22 11:14:36'),
	(5,'etat-demande-1','2022-11-22 13:53:52','2022-11-22 13:54:18','2022-11-22 13:54:18'),
	(6,'cat-user-1','2022-11-22 14:02:45','2022-11-22 14:02:45',NULL),
	(8,'etape-traitement 2','2022-11-22 14:22:17','2022-11-22 14:22:53','2022-11-22 14:22:53'),
	(9,'etape-traitement 1','2022-11-22 14:22:19','2022-11-22 14:22:51','2022-11-22 14:22:51'),
	(12,'cat-user-test','2022-11-24 10:17:34','2022-11-24 10:17:34',NULL),
	(14,'cat-user-test2','2022-11-28 11:05:38','2022-11-28 11:05:48','2022-11-28 11:05:48');

/*!40000 ALTER TABLE `categorie_users` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table code_promos
# ------------------------------------------------------------

DROP TABLE IF EXISTS `code_promos`;

CREATE TABLE `code_promos` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pourcentage` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

LOCK TABLES `code_promos` WRITE;
/*!40000 ALTER TABLE `code_promos` DISABLE KEYS */;

INSERT INTO `code_promos` (`id`, `pourcentage`, `created_at`, `updated_at`, `deleted_at`, `code`)
VALUES
	(1,20,'2022-12-05 16:12:28','2022-12-05 16:13:57',NULL,'JLMKJLK'),
	(4,20,'2022-12-05 16:13:16','2022-12-05 16:13:16',NULL,'JLMKJLKJK'),
	(6,10,'2022-12-05 16:14:16','2022-12-05 16:14:42','2022-12-05 16:14:42','codetpdelete');

/*!40000 ALTER TABLE `code_promos` ENABLE KEYS */;
UNLOCK TABLES;


# Affichage de la table demandes
# ------------------------------------------------------------

DROP TABLE IF EXISTS `demandes`;

CREATE TABLE `demandes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dossier_id` int(11) DEFAULT NULL,
  `champs_demande` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `type_demande_id` int(11) DEFAULT NULL,
  `etape_traitement_id` int(11) DEFAULT NULL,
  `pays_id` int(11) DEFAULT NULL,
  `etat_demande_id` int(11) DEFAULT NULL,
  `numero_demande` varchar(225) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `deleted_at` timestamp NULL DEFAULT NULL,
  `champs_questionnaire` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `champs_etape_traitements` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL,
  `montant_total` int(11) DEFAULT NULL,
  `montant_paye` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_demande` (`numero_demande`),
  KEY `dossier_id` (`dossier_id`),
  KEY `type_demande_id` (`type_demande_id`),
  KEY `etape_traitement_id` (`etape_traitement_id`),
  KEY `pays_id` (`pays_id`),
  KEY `etat_demande_id` (`etat_demande_id`),
  CONSTRAINT `demandes_ibfk_1` FOREIGN KEY (`dossier_id`) REFERENCES `dossiers` (`id`),
  CONSTRAINT `demandes_ibfk_2` FOREIGN KEY (`type_demande_id`) REFERENCES `type_demandes` (`id`),
  CONSTRAINT `demandes_ibfk_3` FOREIGN KEY (`etape_traitement_id`) REFERENCES `etape_traitements` (`id`),
  CONSTRAINT `demandes_ibfk_4` FOREIGN KEY (`pays_id`) REFERENCES `pays` (`id`),
  CONSTRAINT `demandes_ibfk_5` FOREIGN KEY (`etat_demande_id`) REFERENCES `etat_demandes` (`id`),
  CONSTRAINT `demandes_chk_1` CHECK (json_valid(`champs_demande`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

