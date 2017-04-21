CREATE DATABASE  IF NOT EXISTS `trainingplan` /*!40100 DEFAULT CHARACTER SET utf8 COLLATE utf8_slovak_ci */;
USE `trainingplan`;
-- MySQL dump 10.13  Distrib 5.7.17, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: trainingplan
-- ------------------------------------------------------
-- Server version	5.7.17-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `weeklyhours`
--

DROP TABLE IF EXISTS `weeklyhours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `weeklyhours` (
  `annualHours` int(11) NOT NULL,
  `Preparatory-1` float NOT NULL,
  `Base 1-1` float NOT NULL,
  `Base 1-2` float NOT NULL,
  `Base 1-3` float NOT NULL,
  `Base 1-4` float NOT NULL,
  `Base 2-1` float NOT NULL,
  `Base 2-2` float NOT NULL,
  `Base 2-3` float NOT NULL,
  `Base 2-4` float NOT NULL,
  `Base 3-1` float NOT NULL,
  `Base 3-2` float NOT NULL,
  `Base 3-3` float NOT NULL,
  `Base 3-4` float NOT NULL,
  `Build 1-1` float NOT NULL,
  `Build 1-2` float NOT NULL,
  `Build 1-3` float NOT NULL,
  `Build 1-4` float NOT NULL,
  `Build 2-1` float NOT NULL,
  `Build 2-2` float NOT NULL,
  `Build 2-3` float NOT NULL,
  `Build 2-4` float NOT NULL,
  `Peak 1` float NOT NULL,
  `Peak 2` float NOT NULL,
  `Racing-1` float NOT NULL,
  `Recovery-1` float NOT NULL,
  PRIMARY KEY (`annualHours`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_slovak_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-09 22:09:52
