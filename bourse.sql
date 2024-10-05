-- MySQL dump 10.13  Distrib 8.3.0, for Win64 (x86_64)
--
-- Host: localhost    Database: bourse
-- ------------------------------------------------------
-- Server version       8.2.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `action` (
  `idaction` int NOT NULL,
  `societe` varchar(45) NOT NULL,
  `nombre` int NOT NULL,
  `prix` int NOT NULL,
  PRIMARY KEY (`idaction`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action`
--

LOCK TABLES `action` WRITE;
/*!40000 ALTER TABLE `action` DISABLE KEYS */;
INSERT INTO `action` VALUES (1,'Attijariwafa Bank',139,100),(2,'Bank of Africa',0,71),(3,'Bank of Africa',99,27),(4,'CIH Bank',329,66),(5,'Attijariwafa Bank',55,41),(6,'Banque Populaire',252,62),(7,'CIH Bank',297,36),(8,'Bank of Africa',386,97),(9,'Societe generale Maroc',430,98),(10,'Attijariwafa Bank',106,84),(11,'Societe generale Maroc',5,36),(12,'Attijariwafa Bank',299,85),(13,'Attijariwafa Bank',390,67),(14,'Credit du Maroc',305,90),(15,'Credit du Maroc',266,43),(16,'Credit agricole du Maroc',73,12),(17,'Societe generale Maroc',147,79),(18,'Credit du Maroc',140,85),(19,'Banque Populaire',432,25),(20,'Attijariwafa Bank',37,36),(21,'Banque Populaire',62,94),(22,'Credit du Maroc',74,21),(23,'BMCI',471,13),(24,'BMCI',259,11),(25,'BMCI',159,30),(26,'Credit du Maroc',156,51),(27,'Bank of Africa',342,56),(28,'Societe generale Maroc',390,64),(29,'Bank of Africa',246,50),(30,'Attijariwafa Bank',170,32),(31,'Societe generale Maroc',429,88),(32,'Attijariwafa Bank',210,35),(33,'Societe generale Maroc',127,90),(34,'CIH Bank',87,23),(35,'Attijariwafa Bank',494,84),(36,'Bank of Africa',440,20),(37,'Societe generale Maroc',196,68),(38,'Attijariwafa Bank',74,68),(39,'Credit du Maroc',401,15),(40,'BMCI',377,74);
/*!40000 ALTER TABLE `action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `actions_client`
--

DROP TABLE IF EXISTS `actions_client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `actions_client` (
  `idclient` int NOT NULL,
  `idaction` int NOT NULL,
  `nombre` int NOT NULL,
  PRIMARY KEY (`idclient`,`idaction`),
  KEY `idaction_idx` (`idaction`),
  CONSTRAINT `idaction` FOREIGN KEY (`idaction`) REFERENCES `action` (`idaction`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `idclient` FOREIGN KEY (`idclient`) REFERENCES `client` (`idclient`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `actions_client`
--

LOCK TABLES `actions_client` WRITE;
/*!40000 ALTER TABLE `actions_client` DISABLE KEYS */;
INSERT INTO `actions_client` VALUES (1,1,6),(1,2,178),(1,13,2),(1,22,5),(2,1,1),(2,2,4),(2,34,6),(3,12,4);
/*!40000 ALTER TABLE `actions_client` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `client`
--

DROP TABLE IF EXISTS `client`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `client` (
  `idclient` int NOT NULL AUTO_INCREMENT,
  `nom_client` varchar(45) NOT NULL,
  `solde` int DEFAULT NULL,
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`idclient`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `client`
--

LOCK TABLES `client` WRITE;
/*!40000 ALTER TABLE `client` DISABLE KEYS */;
INSERT INTO `client` VALUES (1,'Alice',9986762,'sdx5Li'),(2,'Bob',1639,'Z1DVEH'),(3,'Charlie',2000,'EhmKpI'),(4,'David',2500,'jYQRXn'),(5,'Eve',3000,'nYcX2k');
/*!40000 ALTER TABLE `client` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-05 21:48:15