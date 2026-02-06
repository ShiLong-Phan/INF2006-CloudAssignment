CREATE DATABASE  IF NOT EXISTS `inf2006` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `inf2006`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: inf2006
-- ------------------------------------------------------
-- Server version	8.4.7

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--


--
-- Table structure for table `degrees`
--

DROP TABLE IF EXISTS `degrees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `degrees` (
  `degree_id` int NOT NULL AUTO_INCREMENT,
  `school_id` int NOT NULL,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`degree_id`),
  UNIQUE KEY `school_id` (`school_id`,`name`),
  CONSTRAINT `fk_school` FOREIGN KEY (`school_id`) REFERENCES `schools` (`school_id`)
) ENGINE=InnoDB AUTO_INCREMENT=512 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `employment_outcomes`
--

DROP TABLE IF EXISTS `employment_outcomes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employment_outcomes` (
  `degree_id` int NOT NULL,
  `year` int NOT NULL,
  `employment_rate_overall` decimal(5,2) DEFAULT NULL,
  `employment_rate_ft_perm` decimal(5,2) DEFAULT NULL,
  `basic_monthly_mean` decimal(10,2) DEFAULT NULL,
  `basic_monthly_median` decimal(10,2) DEFAULT NULL,
  `gross_monthly_mean` decimal(10,2) DEFAULT NULL,
  `gross_monthly_median` decimal(10,2) DEFAULT NULL,
  `gross_monthly_25_percentile` decimal(10,2) DEFAULT NULL,
  `gross_monthly_75_percentile` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`degree_id`,`year`),
  KEY `fk_year` (`year`),
  CONSTRAINT `fk_degree` FOREIGN KEY (`degree_id`) REFERENCES `degrees` (`degree_id`),
  CONSTRAINT `fk_year` FOREIGN KEY (`year`) REFERENCES `years` (`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `schools`
--

DROP TABLE IF EXISTS `schools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schools` (
  `school_id` int NOT NULL AUTO_INCREMENT,
  `university_id` int NOT NULL,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`school_id`),
  UNIQUE KEY `university_id` (`university_id`,`name`),
  CONSTRAINT `fk_university` FOREIGN KEY (`university_id`) REFERENCES `universities` (`university_id`)
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `stage_gess`
--

DROP TABLE IF EXISTS `stage_gess`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stage_gess` (
  `university` varchar(500) DEFAULT NULL,
  `school` varchar(500) DEFAULT NULL,
  `degree` varchar(500) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `employment_rate_overall` decimal(10,2) DEFAULT NULL,
  `employment_rate_ft_perm` decimal(10,2) DEFAULT NULL,
  `basic_monthly_mean` decimal(10,2) DEFAULT NULL,
  `basic_monthly_median` decimal(10,2) DEFAULT NULL,
  `gross_monthly_mean` decimal(10,2) DEFAULT NULL,
  `gross_monthly_median` decimal(10,2) DEFAULT NULL,
  `gross_mthly_25_percentile` decimal(10,2) DEFAULT NULL,
  `gross_mthly_75_percentile` decimal(10,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `universities`
--

DROP TABLE IF EXISTS `universities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `universities` (
  `university_id` int NOT NULL AUTO_INCREMENT,
  `university_name` varchar(64) NOT NULL,
  PRIMARY KEY (`university_id`),
  UNIQUE KEY `university_name_UNIQUE` (`university_name`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `years`
--

DROP TABLE IF EXISTS `years`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `years` (
  `year` int NOT NULL,
  PRIMARY KEY (`year`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping routines for database 'inf2006'
--
/*!50003 DROP PROCEDURE IF EXISTS `populate_production_tables` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`admin`@`%` PROCEDURE `populate_production_tables`()
BEGIN
    -- 1. Disable checks to allow truncating parents before children
    SET FOREIGN_KEY_CHECKS = 0;

    -- 2. CLEAN SLATE: Wipe existing production data
    TRUNCATE TABLE employment_outcomes;
    TRUNCATE TABLE degrees;
    TRUNCATE TABLE schools;
    TRUNCATE TABLE universities;
    TRUNCATE TABLE years;

    -- 3. DIMENSIONS: Repopulate from the fresh staging data
    INSERT INTO years (year) 
    SELECT DISTINCT year FROM stage_gess;

    INSERT INTO universities (university_name) 
    SELECT DISTINCT university FROM stage_gess;
    
    INSERT INTO schools (name, university_id)
    SELECT DISTINCT s.school, u.university_id
    FROM stage_gess s
    JOIN universities u ON s.university = u.university_name;

    INSERT INTO degrees (name, school_id)
    SELECT DISTINCT s.degree, sch.school_id
    FROM stage_gess s
    JOIN universities u ON s.university = u.university_name
    JOIN schools sch ON s.school = sch.name AND sch.university_id = u.university_id;

    -- 4. FACT TABLE: Map IDs and load outcomes
    INSERT INTO employment_outcomes (
        degree_id, year, employment_rate_overall, employment_rate_ft_perm, 
        basic_monthly_mean, basic_monthly_median, gross_monthly_mean, 
        gross_monthly_median, gross_monthly_25_percentile, gross_monthly_75_percentile
    )
    SELECT 
        d.degree_id, s.year, s.employment_rate_overall, s.employment_rate_ft_perm,
        s.basic_monthly_mean, s.basic_monthly_median, s.gross_monthly_mean,
        s.gross_monthly_median, s.gross_mthly_25_percentile, s.gross_mthly_75_percentile
    FROM stage_gess s
    JOIN universities u ON s.university = u.university_name
    JOIN schools sch ON s.school = sch.name AND sch.university_id = u.university_id
    JOIN degrees d ON s.degree = d.name AND d.school_id = sch.school_id;

    -- 5. Re-enable checks
    SET FOREIGN_KEY_CHECKS = 1;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-02 16:02:01
