CREATE DATABASE  IF NOT EXISTS `simstore` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `simstore`;
-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: simstore
-- ------------------------------------------------------
-- Server version	8.0.39

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

--
-- Table structure for table `account`
--

DROP TABLE IF EXISTS `account`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `username` varchar(150) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `employee_id` bigint NOT NULL,
  `role_id` bigint NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `employee_id` (`employee_id`),
  KEY `account_role_id_eb09a92c_fk_role_id` (`role_id`),
  CONSTRAINT `account_employee_id_1558cb99_fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  CONSTRAINT `account_role_id_eb09a92c_fk_role_id` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account`
--

LOCK TABLES `account` WRITE;
/*!40000 ALTER TABLE `account` DISABLE KEYS */;
INSERT INTO `account` VALUES (1,'pbkdf2_sha256$870000$iMLUwWGqKWLwduzlue4mjy$8pBwySTV8fakuqdCwdVaSge1yPDvaKuR+a+YyYytSE0=','nvsau',1,1,1,0),(2,'pbkdf2_sha256$870000$CRp8hfneTmKAugcCRnd2u0$2VWhaS4lhj5UVkGEGFkpPjlBgxjLfpCm/uX1YMDA/Mk=','lmsau',1,2,1,1),(3,'pbkdf2_sha256$870000$adtmsjaZx5EstSUwzaRol5$kKYVjJxqLNfhHj37XwI3fHErlIKAgPBOCPGr+7frai4=','vcong',1,3,2,1),(4,'pbkdf2_sha256$870000$e5bgcFEqy8n1rPa7bAJpiP$Feu62Wb3yOTAcfldh7yZa2Poid+IWNtqa/MfBk8gal8=','ttmy',1,4,2,1),(5,'pbkdf2_sha256$870000$orYz5pG5FDNbsyzpEG7BXQ$ukDkQDl3xFKBfVrK11KVoblXGbhr/tKpi7kd1guIvXo=','nson',1,5,2,1),(6,'pbkdf2_sha256$870000$A6EpElXxMBGxze46EFdbMc$Fin1UqldQMJ/7hrgjIh/Czl4+yxn9GQDo88ICsxZ+jI=','KinKin2412',1,7,1,1);
/*!40000 ALTER TABLE `account` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_groups`
--

DROP TABLE IF EXISTS `account_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_groups_account_id_group_id_59cc89ca_uniq` (`account_id`,`group_id`),
  KEY `account_groups_group_id_a67ded22_fk_auth_group_id` (`group_id`),
  CONSTRAINT `account_groups_account_id_d9b57185_fk_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `account_groups_group_id_a67ded22_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_groups`
--

LOCK TABLES `account_groups` WRITE;
/*!40000 ALTER TABLE `account_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `account_user_permissions`
--

DROP TABLE IF EXISTS `account_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `account_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `account_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `account_user_permissions_account_id_permission_id_a6d962f2_uniq` (`account_id`,`permission_id`),
  KEY `account_user_permiss_permission_id_a1087168_fk_auth_perm` (`permission_id`),
  CONSTRAINT `account_user_permiss_permission_id_a1087168_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `account_user_permissions_account_id_5d542d01_fk_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `account_user_permissions`
--

LOCK TABLES `account_user_permissions` WRITE;
/*!40000 ALTER TABLE `account_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `account_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add blacklisted token',6,'add_blacklistedtoken'),(22,'Can change blacklisted token',6,'change_blacklistedtoken'),(23,'Can delete blacklisted token',6,'delete_blacklistedtoken'),(24,'Can view blacklisted token',6,'view_blacklistedtoken'),(25,'Can add outstanding token',7,'add_outstandingtoken'),(26,'Can change outstanding token',7,'change_outstandingtoken'),(27,'Can delete outstanding token',7,'delete_outstandingtoken'),(28,'Can view outstanding token',7,'view_outstandingtoken'),(29,'Can add employee',8,'add_employee'),(30,'Can change employee',8,'change_employee'),(31,'Can delete employee',8,'delete_employee'),(32,'Can view employee',8,'view_employee'),(33,'Can add role',9,'add_role'),(34,'Can change role',9,'change_role'),(35,'Can delete role',9,'delete_role'),(36,'Can view role',9,'view_role'),(37,'Can add account',10,'add_account'),(38,'Can change account',10,'change_account'),(39,'Can delete account',10,'delete_account'),(40,'Can view account',10,'view_account'),(41,'Can add supplier',11,'add_supplier'),(42,'Can change supplier',11,'change_supplier'),(43,'Can delete supplier',11,'delete_supplier'),(44,'Can view supplier',11,'view_supplier'),(45,'Can add import receipt',12,'add_importreceipt'),(46,'Can change import receipt',12,'change_importreceipt'),(47,'Can delete import receipt',12,'delete_importreceipt'),(48,'Can view import receipt',12,'view_importreceipt'),(49,'Can add import receipt detail',13,'add_importreceiptdetail'),(50,'Can change import receipt detail',13,'change_importreceiptdetail'),(51,'Can delete import receipt detail',13,'delete_importreceiptdetail'),(52,'Can view import receipt detail',13,'view_importreceiptdetail'),(53,'Can add category1',14,'add_category1'),(54,'Can change category1',14,'change_category1'),(55,'Can delete category1',14,'delete_category1'),(56,'Can view category1',14,'view_category1'),(57,'Can add category2',15,'add_category2'),(58,'Can change category2',15,'change_category2'),(59,'Can delete category2',15,'delete_category2'),(60,'Can view category2',15,'view_category2'),(61,'Can add mobile network operator',16,'add_mobilenetworkoperator'),(62,'Can change mobile network operator',16,'change_mobilenetworkoperator'),(63,'Can delete mobile network operator',16,'delete_mobilenetworkoperator'),(64,'Can view mobile network operator',16,'view_mobilenetworkoperator'),(65,'Can add sim',17,'add_sim'),(66,'Can change sim',17,'change_sim'),(67,'Can delete sim',17,'delete_sim'),(68,'Can view sim',17,'view_sim'),(69,'Can add customer',18,'add_customer'),(70,'Can change customer',18,'change_customer'),(71,'Can delete customer',18,'delete_customer'),(72,'Can view customer',18,'view_customer'),(73,'Can add discount',19,'add_discount'),(74,'Can change discount',19,'change_discount'),(75,'Can delete discount',19,'delete_discount'),(76,'Can view discount',19,'view_discount'),(77,'Can add order',20,'add_order'),(78,'Can change order',20,'change_order'),(79,'Can delete order',20,'delete_order'),(80,'Can view order',20,'view_order'),(81,'Can add province',21,'add_province'),(82,'Can change province',21,'change_province'),(83,'Can delete province',21,'delete_province'),(84,'Can view province',21,'view_province'),(85,'Can add district',22,'add_district'),(86,'Can change district',22,'change_district'),(87,'Can delete district',22,'delete_district'),(88,'Can view district',22,'view_district'),(89,'Can add ward',23,'add_ward'),(90,'Can change ward',23,'change_ward'),(91,'Can delete ward',23,'delete_ward'),(92,'Can view ward',23,'view_ward'),(93,'Can add detail update order',24,'add_detailupdateorder'),(94,'Can change detail update order',24,'change_detailupdateorder'),(95,'Can delete detail update order',24,'delete_detailupdateorder'),(96,'Can view detail update order',24,'view_detailupdateorder'),(97,'Can add payment',25,'add_payment'),(98,'Can change payment',25,'change_payment'),(99,'Can delete payment',25,'delete_payment'),(100,'Can view payment',25,'view_payment'),(101,'Can add Password Reset Token',26,'add_resetpasswordtoken'),(102,'Can change Password Reset Token',26,'change_resetpasswordtoken'),(103,'Can delete Password Reset Token',26,'delete_resetpasswordtoken'),(104,'Can view Password Reset Token',26,'view_resetpasswordtoken');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category1`
--

DROP TABLE IF EXISTS `category1`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category1` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category1`
--

LOCK TABLES `category1` WRITE;
/*!40000 ALTER TABLE `category1` DISABLE KEYS */;
INSERT INTO `category1` VALUES (1,'Cam Kết',''),(2,'Trả Trước',''),(3,'Trả Sau','');
/*!40000 ALTER TABLE `category1` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category2`
--

DROP TABLE IF EXISTS `category2`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category2` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category2`
--

LOCK TABLES `category2` WRITE;
/*!40000 ALTER TABLE `category2` DISABLE KEYS */;
INSERT INTO `category2` VALUES (1,'Số đẹp',''),(2,'Siêu vip',''),(3,'Lục Quý',''),(4,'Ngũ Quý',''),(5,'Tứ Quý',''),(6,'Tam Hoa',''),(7,'Số Kép','');
/*!40000 ALTER TABLE `category2` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(254) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Nguyễn Văn A','09999999999','nvana@gmail.com','2025-03-05 09:58:09.825724'),(2,'Nguyễn Văn A','076478415',NULL,'2025-03-05 10:04:32.253937'),(3,'Nguyễn Văn A','0764799251',NULL,'2025-03-05 10:04:52.221082'),(4,'Nguyễn Văn A','0764784251',NULL,'2025-03-05 14:07:40.646772'),(5,'Lý Mặc Sầu','0764784251',NULL,'2025-03-05 14:08:01.345965'),(7,'Phan Văn Trị','0764784251',NULL,'2025-03-05 14:20:25.908671'),(9,'Nguyễn Văn A','0764784251',NULL,'2025-03-05 14:41:17.532409'),(25,'Trần Văn Sửu','0764784214',NULL,'2025-03-10 09:16:32.162753'),(26,'Trần Văn Sửu','0764784214',NULL,'2025-03-10 09:51:05.493614'),(28,'Lâm Văn Tài','076472142515','lvtai@gmail.com','2025-03-10 10:14:10.292759'),(29,'Lê Tấn Lợi','07642515','ltloi@gmail.com','2025-03-10 10:14:47.965866'),(32,'Lê Thị Đậu','0764784214',NULL,'2025-03-11 12:29:47.650612');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detail_update_order`
--

DROP TABLE IF EXISTS `detail_update_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detail_update_order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `updated_at` datetime(6) NOT NULL,
  `status_updated` int NOT NULL,
  `employee_id` bigint NOT NULL,
  `order_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `detail_update_order_employee_id_de18a155_fk_employee_id` (`employee_id`),
  KEY `detail_update_order_order_id_41c9d2dc_fk_order_id` (`order_id`),
  CONSTRAINT `detail_update_order_employee_id_de18a155_fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  CONSTRAINT `detail_update_order_order_id_41c9d2dc_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detail_update_order`
--

LOCK TABLES `detail_update_order` WRITE;
/*!40000 ALTER TABLE `detail_update_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `detail_update_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `discount`
--

DROP TABLE IF EXISTS `discount`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `discount` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `percentage` decimal(5,2) NOT NULL,
  `start_date` datetime(6) NOT NULL,
  `end_date` datetime(6) NOT NULL,
  `description` longtext,
  `status` tinyint(1) NOT NULL,
  `employee_id` bigint NOT NULL,
  `discount_code` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `discount_created_by_id_f4092736` (`employee_id`),
  CONSTRAINT `discount_employee_id_d3c9de89_fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `discount`
--

LOCK TABLES `discount` WRITE;
/*!40000 ALTER TABLE `discount` DISABLE KEYS */;
INSERT INTO `discount` VALUES (1,10.00,'2025-03-01 00:00:00.000000','2025-03-31 23:59:59.000000','Giảm 10% cho khách hàng mới',0,1,''),(2,20.00,'2025-03-10 00:00:00.000000','2025-03-20 23:59:59.000000','Ưu đãi 20% khi đặt hàng online',0,2,''),(3,50.00,'2025-03-01 00:00:00.000000','2025-04-30 23:59:59.000000','Giảm 50% cho đơn hàng trên 1 triệu',0,3,''),(5,15.00,'2024-03-05 00:00:00.000000','2024-04-05 23:59:59.000000','Giảm 15% cho khách hàng thân thiết',0,5,''),(6,30.00,'2024-03-01 00:00:00.000000','2024-03-31 23:59:59.000000','Khuyến mãi 30% dịp sinh nhật',1,6,''),(7,0.00,'2024-02-01 00:00:00.000000','2024-02-28 23:59:59.000000','Mã giảm giá đã sử dụng',0,7,''),(8,20.00,'2025-03-15 13:46:00.000000','2025-03-21 13:46:00.000000','',0,1,'MGG1203258'),(9,15.00,'2025-03-05 13:46:00.000000','2025-03-21 13:46:00.000000','Giảm giá 15%',0,4,'MGG1203259'),(11,50.00,'2025-03-13 08:30:00.000000','2025-06-04 23:59:59.000000','Khuyến mãi tháng 3',1,5,'MGG13032511');
/*!40000 ALTER TABLE `discount` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `district`
--

DROP TABLE IF EXISTS `district`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `district` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `province_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `district_province_id_2f524890_fk_province_id` (`province_id`),
  CONSTRAINT `district_province_id_2f524890_fk_province_id` FOREIGN KEY (`province_id`) REFERENCES `province` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `district`
--

LOCK TABLES `district` WRITE;
/*!40000 ALTER TABLE `district` DISABLE KEYS */;
INSERT INTO `district` VALUES (1,'Quận 1',30),(2,'Quận 3',30),(3,'Quận 5',30),(4,'Quận 7',30),(5,'Quận Bình Thạnh',30),(6,'Quận Gò Vấp',30),(7,'Huyện Bình Chánh',30),(8,'Huyện Củ Chi',30),(9,'Quận Ba Đình',24),(10,'Quận Hoàn Kiếm',24),(11,'Quận Hai Bà Trưng',24),(12,'Quận Đống Đa',24),(13,'Quận Cầu Giấy',24),(14,'Quận Thanh Xuân',24),(15,'Quận Long Biên',24),(16,'Quận Nam Từ Liêm',24),(17,'Quận Bắc Từ Liêm',24),(18,'Quận Hà Đông',24),(19,'Huyện Gia Lâm',24),(20,'Huyện Đông Anh',24),(21,'Huyện Sóc Sơn',24),(22,'Huyện Thanh Trì',24),(23,'Quận Hải Châu',15),(24,'Quận Thanh Khê',15),(25,'Quận Sơn Trà',15),(26,'Quận Ngũ Hành Sơn',15),(27,'Quận Liên Chiểu',15),(28,'Huyện Hòa Vang',15),(29,'Thành phố Biên Hòa',19),(30,'Thành phố Long Khánh',19),(31,'Huyện Nhơn Trạch',19),(32,'Huyện Trảng Bom',19),(33,'Huyện Long Thành',19),(34,'Huyện Vĩnh Cửu',19),(35,'Thành phố Thủ Dầu Một',17),(36,'Thành phố Thuận An',17),(37,'Thành phố Dĩ An',17),(38,'Huyện Bến Cát',17),(39,'Huyện Tân Uyên',17),(40,'Thành phố Nha Trang',21),(41,'Thành phố Cam Ranh',21),(42,'Huyện Vạn Ninh',21),(43,'Huyện Diên Khánh',21),(44,'Huyện Cam Lâm',21),(45,'Huyện Khánh Vĩnh',21),(46,'Thành phố Huế',26),(47,'Huyện Phú Vang',26),(48,'Huyện Hương Trà',26),(49,'Huyện Hương Thủy',26),(50,'Thành phố Đà Lạt',14),(51,'Thành phố Bảo Lộc',14),(52,'Huyện Di Linh',14),(53,'Huyện Lạc Dương',14),(54,'Huyện Đức Trọng',14),(55,'Thành phố Vũng Tàu',18),(56,'Thành phố Bà Rịa',18),(57,'Huyện Long Điền',18),(58,'Huyện Đất Đỏ',18),(59,'Huyện Xuyên Mộc',18),(60,'Thành phố Cần Thơ',31),(61,'Quận Ninh Kiều',31),(62,'Quận Bình Thủy',31),(63,'Huyện Cờ Đỏ',31),(64,'Huyện Thới Lai',31);
/*!40000 ALTER TABLE `district` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_account_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_account_id` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (10,'accounts','account'),(8,'accounts','employee'),(9,'accounts','role'),(1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'contenttypes','contenttype'),(26,'django_rest_passwordreset','resetpasswordtoken'),(22,'locations','district'),(21,'locations','province'),(23,'locations','ward'),(18,'orders','customer'),(24,'orders','detailupdateorder'),(19,'orders','discount'),(20,'orders','order'),(25,'orders','payment'),(5,'sessions','session'),(14,'simcards','category1'),(15,'simcards','category2'),(16,'simcards','mobilenetworkoperator'),(17,'simcards','sim'),(12,'suppliers','importreceipt'),(13,'suppliers','importreceiptdetail'),(11,'suppliers','supplier'),(6,'token_blacklist','blacklistedtoken'),(7,'token_blacklist','outstandingtoken');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-03-04 16:09:37.218215'),(2,'contenttypes','0002_remove_content_type_name','2025-03-04 16:09:37.300009'),(3,'auth','0001_initial','2025-03-04 16:09:37.632019'),(4,'auth','0002_alter_permission_name_max_length','2025-03-04 16:09:37.705153'),(5,'auth','0003_alter_user_email_max_length','2025-03-04 16:09:37.712213'),(6,'auth','0004_alter_user_username_opts','2025-03-04 16:09:37.718142'),(7,'auth','0005_alter_user_last_login_null','2025-03-04 16:09:37.726190'),(8,'auth','0006_require_contenttypes_0002','2025-03-04 16:09:37.730086'),(9,'auth','0007_alter_validators_add_error_messages','2025-03-04 16:09:37.738596'),(10,'auth','0008_alter_user_username_max_length','2025-03-04 16:09:37.747198'),(11,'auth','0009_alter_user_last_name_max_length','2025-03-04 16:09:37.754294'),(12,'auth','0010_alter_group_name_max_length','2025-03-04 16:09:37.772842'),(13,'auth','0011_update_proxy_permissions','2025-03-04 16:09:37.780933'),(14,'auth','0012_alter_user_first_name_max_length','2025-03-04 16:09:37.789997'),(15,'accounts','0001_initial','2025-03-04 16:09:38.473984'),(16,'accounts','0002_alter_account_employee_alter_employee_citizen_id_and_more','2025-03-04 16:09:38.713781'),(17,'accounts','0003_alter_account_employee','2025-03-04 16:09:38.721891'),(18,'accounts','0004_alter_account_role','2025-03-04 16:09:38.731523'),(19,'accounts','0005_alter_employee_gender','2025-03-04 16:09:38.815437'),(20,'admin','0001_initial','2025-03-04 16:09:38.980848'),(21,'admin','0002_logentry_remove_auto_add','2025-03-04 16:09:38.988941'),(22,'admin','0003_logentry_add_action_flag_choices','2025-03-04 16:09:38.999394'),(23,'locations','0001_initial','2025-03-04 16:09:39.197100'),(24,'locations','0002_alter_district_name_alter_province_name_and_more','2025-03-04 16:09:39.240019'),(25,'locations','0003_alter_district_province_alter_ward_district','2025-03-04 16:09:39.248526'),(26,'simcards','0001_initial','2025-03-04 16:09:39.689807'),(27,'orders','0001_initial','2025-03-04 16:09:40.055494'),(28,'orders','0002_alter_customer_phone_number_and_more','2025-03-04 16:09:40.252984'),(29,'orders','0003_rename_created_by_discount_employee','2025-03-04 16:09:40.378042'),(30,'sessions','0001_initial','2025-03-04 16:09:40.419990'),(31,'simcards','0002_alter_sim_export_price','2025-03-04 16:09:40.506264'),(32,'suppliers','0001_initial','2025-03-04 16:09:40.904203'),(33,'suppliers','0002_alter_importreceiptdetail_unique_together_and_more','2025-03-04 16:09:40.981892'),(34,'token_blacklist','0001_initial','2025-03-04 16:09:41.205275'),(35,'token_blacklist','0002_outstandingtoken_jti_hex','2025-03-04 16:09:41.238836'),(36,'token_blacklist','0003_auto_20171017_2007','2025-03-04 16:09:41.259878'),(37,'token_blacklist','0004_auto_20171017_2013','2025-03-04 16:09:41.343958'),(38,'token_blacklist','0005_remove_outstandingtoken_jti','2025-03-04 16:09:41.415409'),(39,'token_blacklist','0006_auto_20171017_2113','2025-03-04 16:09:41.443757'),(40,'token_blacklist','0007_auto_20171017_2214','2025-03-04 16:09:41.681216'),(41,'token_blacklist','0008_migrate_to_bigautofield','2025-03-04 16:09:41.975981'),(42,'token_blacklist','0010_fix_migrate_to_bigautofield','2025-03-04 16:09:41.993930'),(43,'token_blacklist','0011_linearizes_history','2025-03-04 16:09:41.998967'),(44,'token_blacklist','0012_alter_outstandingtoken_user','2025-03-04 16:09:42.018088'),(45,'accounts','0005_account_status','2025-03-05 08:09:21.367942'),(46,'simcards','0003_sim_type','2025-03-05 08:09:21.421360'),(47,'orders','0004_remove_order_payment_methods_order_total_price_and_more','2025-03-05 09:56:11.476089'),(48,'orders','0005_alter_customer_phone_number','2025-03-05 14:07:28.158438'),(49,'orders','0006_alter_order_discount','2025-03-05 14:39:13.355841'),(50,'orders','0007_alter_order_discount','2025-03-07 09:24:02.166029'),(51,'orders','0008_alter_payment_payment_method','2025-03-10 10:28:26.096015'),(52,'simcards','0004_alter_sim_status','2025-03-10 10:28:26.257079'),(53,'orders','0009_payment_updated_at','2025-03-10 15:27:18.141702'),(54,'orders','0010_remove_order_updated_at','2025-03-11 13:49:07.987947'),(55,'orders','0011_discount_discount_code','2025-03-12 13:45:37.709591'),(56,'orders','0012_alter_discount_status','2025-03-13 14:02:34.610093'),(57,'django_rest_passwordreset','0001_initial','2025-03-13 15:52:49.478514'),(58,'django_rest_passwordreset','0002_pk_migration','2025-03-13 15:52:49.724630'),(59,'django_rest_passwordreset','0003_allow_blank_and_null_fields','2025-03-13 15:52:49.799694'),(60,'django_rest_passwordreset','0004_alter_resetpasswordtoken_user_agent','2025-03-13 15:52:49.819387');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_rest_passwordreset_resetpasswordtoken`
--

DROP TABLE IF EXISTS `django_rest_passwordreset_resetpasswordtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_rest_passwordreset_resetpasswordtoken` (
  `created_at` datetime(6) NOT NULL,
  `key` varchar(64) NOT NULL,
  `ip_address` char(39) DEFAULT NULL,
  `user_agent` varchar(512) NOT NULL,
  `user_id` bigint NOT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_rest_passwordreset_resetpasswordtoken_key_f1b65873_uniq` (`key`),
  KEY `django_rest_password_user_id_e8015b11_fk_account_i` (`user_id`),
  CONSTRAINT `django_rest_password_user_id_e8015b11_fk_account_i` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_rest_passwordreset_resetpasswordtoken`
--

LOCK TABLES `django_rest_passwordreset_resetpasswordtoken` WRITE;
/*!40000 ALTER TABLE `django_rest_passwordreset_resetpasswordtoken` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_rest_passwordreset_resetpasswordtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `employee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` tinyint(1) NOT NULL,
  `citizen_id` varchar(12) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `avatar` varchar(100) DEFAULT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `employee_citizen_id_498204b8_uniq` (`citizen_id`),
  UNIQUE KEY `employee_phone_number_e2f6abef_uniq` (`phone_number`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES (1,'Nguyễn Văn Sâu','2003-01-05',1,'992121212122','0654215200','n21dccn122@student.ptithcm.edu.vn','Quận 1','',0),(2,'Lý Mạc Sầu','2000-01-04',1,'992121212155','0654215219','lmsau@gmail.com','Thủ Đức','',1),(3,'Văn Công','1996-01-05',1,'112121212291','0764708152','vcong@gmail.com','Quận 5','',1),(4,'Trần Tiểu Mỹ','2006-06-06',0,'992121212179','0764708184','ttmy@gmail.com','Quận 12','avatars/430222073_3831813897102041_2517065155638459309_n_DrRL5mx.jpg',0),(5,'Nguyễn Sơn','1990-10-30',1,'098743565456','0978907867','sonnguyen@gmail.com','97 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',1),(6,'Trần Thị Anh','1991-08-26',0,'087956789045','0965478965','anhtran@gmail.com','98 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',0),(7,'Nguyễn Hoàng Tiến','1994-07-23',1,'077890564756','0998567435','tiennguyen@gmail.com','90 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',1),(8,'Trần Thị Dung','1995-05-24',0,'067876756789','0932456789','dungtran@gmail.com','91 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',0);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `importreceipt`
--

DROP TABLE IF EXISTS `importreceipt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `importreceipt` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `note` longtext,
  `employee_id` bigint NOT NULL,
  `supplier_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `importReceipt_employee_id_b4a8948a_fk_employee_id` (`employee_id`),
  KEY `importReceipt_supplier_id_cc573533_fk_supplier_id` (`supplier_id`),
  CONSTRAINT `importReceipt_employee_id_b4a8948a_fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  CONSTRAINT `importReceipt_supplier_id_cc573533_fk_supplier_id` FOREIGN KEY (`supplier_id`) REFERENCES `supplier` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `importreceipt`
--

LOCK TABLES `importreceipt` WRITE;
/*!40000 ALTER TABLE `importreceipt` DISABLE KEYS */;
INSERT INTO `importreceipt` VALUES (1,'2025-03-07 15:27:20.872263','Nhập lô SIM mới',2,1),(2,'2025-03-07 15:28:16.076379','Nhập lô SIM mới',2,1),(3,'2025-03-07 15:42:55.599704','Nhập lô SIM mới',2,1),(4,'2025-03-07 15:54:19.118589','Nhập hàng đợt 1',2,1),(5,'2025-03-10 10:27:43.073512','Nhập hàng đợt 1',2,1);
/*!40000 ALTER TABLE `importreceipt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `importreceiptdetail`
--

DROP TABLE IF EXISTS `importreceiptdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `importreceiptdetail` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `import_price` decimal(10,2) NOT NULL,
  `import_receipt_id` bigint NOT NULL,
  `sim_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_import_sim` (`import_receipt_id`,`sim_id`),
  KEY `importReceiptDetail_sim_id_daf2260d_fk_sim_id` (`sim_id`),
  KEY `importReceiptDetail_import_receipt_id_a3254f28` (`import_receipt_id`),
  CONSTRAINT `importReceiptDetail_import_receipt_id_a3254f28_fk_importRec` FOREIGN KEY (`import_receipt_id`) REFERENCES `importreceipt` (`id`),
  CONSTRAINT `importReceiptDetail_sim_id_daf2260d_fk_sim_id` FOREIGN KEY (`sim_id`) REFERENCES `sim` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `importreceiptdetail`
--

LOCK TABLES `importreceiptdetail` WRITE;
/*!40000 ALTER TABLE `importreceiptdetail` DISABLE KEYS */;
INSERT INTO `importreceiptdetail` VALUES (1,5000.00,1,21),(2,0.00,1,22),(3,0.00,2,23),(4,0.00,2,24),(5,0.00,3,25),(6,0.00,3,26),(7,10000.00,4,27),(8,10000.00,4,28),(9,100000.00,5,29),(10,250000.00,5,30);
/*!40000 ALTER TABLE `importreceiptdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mobilenetworkoperator`
--

DROP TABLE IF EXISTS `mobilenetworkoperator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mobilenetworkoperator` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mobilenetworkoperator`
--

LOCK TABLES `mobilenetworkoperator` WRITE;
/*!40000 ALTER TABLE `mobilenetworkoperator` DISABLE KEYS */;
INSERT INTO `mobilenetworkoperator` VALUES (5,'Gmobile'),(2,'Mobifone'),(4,'Vietnammobile'),(3,'Viettel'),(1,'Vinaphone');
/*!40000 ALTER TABLE `mobilenetworkoperator` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order`
--

DROP TABLE IF EXISTS `order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `status_order` int NOT NULL,
  `detailed_address` varchar(255) NOT NULL,
  `note` varchar(500) DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `customer_id` bigint NOT NULL,
  `discount_id` bigint DEFAULT NULL,
  `sim_id` bigint NOT NULL,
  `ward_id` bigint NOT NULL,
  `total_price` decimal(10,2) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_discount_id_821f83e4_uniq` (`discount_id`),
  KEY `order_customer_id_9da9253f_fk_customer_id` (`customer_id`),
  KEY `order_sim_id_84b65407_fk_sim_id` (`sim_id`),
  KEY `order_ward_id_42f7af1f_fk_ward_id` (`ward_id`),
  CONSTRAINT `order_customer_id_9da9253f_fk_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`),
  CONSTRAINT `order_discount_id_821f83e4_fk_discount_id` FOREIGN KEY (`discount_id`) REFERENCES `discount` (`id`),
  CONSTRAINT `order_sim_id_84b65407_fk_sim_id` FOREIGN KEY (`sim_id`) REFERENCES `sim` (`id`),
  CONSTRAINT `order_ward_id_42f7af1f_fk_ward_id` FOREIGN KEY (`ward_id`) REFERENCES `ward` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order`
--

LOCK TABLES `order` WRITE;
/*!40000 ALTER TABLE `order` DISABLE KEYS */;
INSERT INTO `order` VALUES (1,1,'123 Đường ABC, TP.HCM','Giao hàng trong giờ hành chính','2025-03-05 10:04:52.237085',3,NULL,1,3,5000000.00),(2,1,'123 Đường ABC, TP.HCM','Giao hàng trong giờ hành chính','2025-03-05 14:20:25.911671',7,NULL,1,3,5000000.00),(3,1,'123 Đường ABC, TP.HCM','Giao hàng trong giờ hành chính','2025-03-05 14:41:17.537407',9,2,1,3,-95000000.00),(4,1,'92/12 Lê Văn Việt','Giao trước 10h sáng','2025-03-10 09:16:32.177752',25,3,1,3,2500000.00),(5,1,'92/12 Lê Văn Việt','Giao trước 10h sáng','2025-03-10 09:51:05.516584',26,NULL,1,3,5000000.00),(7,1,'Lê Văn Việt','Giao trước buổi tối','2025-03-10 10:14:10.295758',28,NULL,1,3,5000000.00),(8,1,'Lê Văn Việt','Giao trước buổi tối','2025-03-10 10:14:47.968868',29,NULL,5,3,1500000.00),(10,1,'Lê Văn Việt','','2025-03-11 12:29:47.655119',32,NULL,15,3,7500000.00);
/*!40000 ALTER TABLE `order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS `payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `payment_method` varchar(50) NOT NULL,
  `status` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `order_id` bigint NOT NULL,
  `updated_at` datetime(6) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `payment_order_id_98f7562d_fk_order_id` (`order_id`),
  CONSTRAINT `payment_order_id_98f7562d_fk_order_id` FOREIGN KEY (`order_id`) REFERENCES `order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment`
--

LOCK TABLES `payment` WRITE;
/*!40000 ALTER TABLE `payment` DISABLE KEYS */;
INSERT INTO `payment` VALUES (1,'cash',1,'2025-03-10 09:51:05.519582',5,NULL),(2,'cash',1,'2025-03-10 10:14:10.296757',7,'2025-03-10 15:58:02.245794'),(3,'cash',1,'2025-03-10 10:14:47.968868',8,'2025-03-11 12:21:51.142810'),(4,'transfer',0,'2025-03-11 12:29:47.657153',10,NULL);
/*!40000 ALTER TABLE `payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `province`
--

DROP TABLE IF EXISTS `province`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `province` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=64 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `province`
--

LOCK TABLES `province` WRITE;
/*!40000 ALTER TABLE `province` DISABLE KEYS */;
INSERT INTO `province` VALUES (1,'An Giang'),(2,'Bà Rịa - Vũng Tàu'),(3,'Bạc Liêu'),(4,'Bắc Giang'),(5,'Bắc Kạn'),(6,'Bắc Ninh'),(7,'Bến Tre'),(8,'Bình Định'),(9,'Bình Dương'),(10,'Bình Phước'),(11,'Bình Thuận'),(12,'Cà Mau'),(13,'Cần Thơ'),(14,'Cao Bằng'),(15,'Đà Nẵng'),(16,'Đắk Lắk'),(17,'Đắk Nông'),(18,'Điện Biên'),(19,'Đồng Nai'),(20,'Đồng Tháp'),(21,'Gia Lai'),(22,'Hà Giang'),(23,'Hà Nam'),(24,'Hà Nội'),(25,'Hà Tĩnh'),(26,'Hải Dương'),(27,'Hải Phòng'),(28,'Hậu Giang'),(29,'Hòa Bình'),(30,'Hồ Chí Minh'),(31,'Hưng Yên'),(32,'Khánh Hòa'),(33,'Kiên Giang'),(34,'Kon Tum'),(35,'Lai Châu'),(36,'Lâm Đồng'),(37,'Lạng Sơn'),(38,'Lào Cai'),(39,'Long An'),(40,'Nam Định'),(41,'Nghệ An'),(42,'Ninh Bình'),(43,'Ninh Thuận'),(44,'Phú Thọ'),(45,'Phú Yên'),(46,'Quảng Bình'),(47,'Quảng Nam'),(48,'Quảng Ngãi'),(49,'Quảng Ninh'),(50,'Quảng Trị'),(51,'Sóc Trăng'),(52,'Sơn La'),(53,'Tây Ninh'),(54,'Thái Bình'),(55,'Thái Nguyên'),(56,'Thanh Hóa'),(57,'Thừa Thiên Huế'),(58,'Tiền Giang'),(59,'Trà Vinh'),(60,'Tuyên Quang'),(61,'Vĩnh Long'),(62,'Vĩnh Phúc'),(63,'Yên Bái');
/*!40000 ALTER TABLE `province` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `role_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role_name` (`role_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin'),(2,'staff');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sim`
--

DROP TABLE IF EXISTS `sim`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sim` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `phone_number` varchar(15) NOT NULL,
  `export_price` decimal(10,2) DEFAULT NULL,
  `status` int NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `category_1_id` bigint NOT NULL,
  `category_2_id` bigint NOT NULL,
  `employee_id` bigint DEFAULT NULL,
  `mobile_network_operator_id` bigint NOT NULL,
  `type` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_number` (`phone_number`),
  KEY `sim_category_1_id_170735b5_fk_category1_id` (`category_1_id`),
  KEY `sim_category_2_id_262e9e05_fk_category2_id` (`category_2_id`),
  KEY `sim_employee_id_369193cc_fk_employee_id` (`employee_id`),
  KEY `sim_mobile_network_opera_211a56d6_fk_mobileNet` (`mobile_network_operator_id`),
  CONSTRAINT `sim_category_1_id_170735b5_fk_category1_id` FOREIGN KEY (`category_1_id`) REFERENCES `category1` (`id`),
  CONSTRAINT `sim_category_2_id_262e9e05_fk_category2_id` FOREIGN KEY (`category_2_id`) REFERENCES `category2` (`id`),
  CONSTRAINT `sim_employee_id_369193cc_fk_employee_id` FOREIGN KEY (`employee_id`) REFERENCES `employee` (`id`),
  CONSTRAINT `sim_mobile_network_opera_211a56d6_fk_mobileNet` FOREIGN KEY (`mobile_network_operator_id`) REFERENCES `mobilenetworkoperator` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=31 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sim`
--

LOCK TABLES `sim` WRITE;
/*!40000 ALTER TABLE `sim` DISABLE KEYS */;
INSERT INTO `sim` VALUES (1,'0987654321',5000000.00,0,'2025-02-12 10:00:00.000000',1,4,1,3,'physical'),(2,'0971234567',2000000.00,2,'2025-02-13 03:14:00.000000',2,6,2,3,'qr'),(3,'0912345678',8000000.00,0,'2025-02-14 03:14:00.000000',3,1,3,1,'physical'),(4,'0908765432',3000000.00,1,'2025-02-15 03:14:00.000000',2,5,4,2,'qr'),(5,'0931122334',1500000.00,2,'2025-02-16 03:14:00.000000',1,2,5,2,'physical'),(6,'0321456789',1200000.00,1,'2025-02-17 03:14:00.000000',3,7,1,4,'qr'),(7,'0869998888',9500000.00,0,'2025-02-18 03:14:00.000000',1,6,2,5,'physical'),(8,'0886665555',4000000.00,2,'2025-02-19 03:14:00.000000',2,4,3,3,'qr'),(9,'0897774444',6000000.00,1,'2025-02-20 03:14:00.000000',3,5,4,3,'physical'),(10,'0963332222',7000000.00,0,'2025-02-21 03:14:00.000000',1,3,1,1,'qr'),(11,'0945551111',2200000.00,1,'2025-02-22 03:14:00.000000',2,6,2,1,'physical'),(12,'0924447777',3500000.00,2,'2025-02-23 03:14:00.000000',3,7,3,2,'qr'),(13,'0341119999',5000000.00,1,'2025-02-24 03:14:00.000000',1,2,4,4,'physical'),(14,'0352228888',4200000.00,0,'2025-02-25 03:14:00.000000',2,3,2,4,'qr'),(15,'0363337777',7500000.00,2,'2025-02-26 03:14:00.000000',3,1,1,4,'physical'),(16,'0374446666',1300000.00,1,'2025-02-27 03:14:00.000000',1,4,4,5,'qr'),(17,'0385555555',2700000.00,0,'2025-02-28 03:14:00.000000',2,6,3,5,'physical'),(18,'0396664444',3000000.00,0,'2025-03-01 03:14:00.000000',3,7,4,5,'qr'),(19,'0707773333',5000000.00,1,'2025-03-02 03:14:00.000000',1,2,5,2,'physical'),(20,'0778882222',6500000.00,0,'2025-03-03 03:14:00.000000',2,5,5,3,'qr'),(21,'0954175448',NULL,1,'2025-03-07 15:27:20.887945',2,3,2,1,'physical'),(22,'0933256885',NULL,1,'2025-03-07 15:27:20.908858',2,4,2,1,'physical'),(23,'0918124754',NULL,1,'2025-03-07 15:28:16.080383',2,3,2,1,'physical'),(24,'021548548475',NULL,1,'2025-03-07 15:28:16.088017',2,4,2,1,'physical'),(25,'0954175784',NULL,1,'2025-03-07 15:42:55.604973',2,3,2,1,'qr'),(26,'0933843885',NULL,1,'2025-03-07 15:42:55.611836',2,4,2,1,'qr'),(27,'0951575784',NULL,1,'2025-03-07 15:54:19.133666',2,3,2,1,'qr'),(28,'0954179244',NULL,1,'2025-03-07 15:54:19.140664',2,3,2,1,'qr'),(29,'0951174784',NULL,1,'2025-03-10 10:27:43.087745',2,3,2,1,'qr'),(30,'0954178164',NULL,1,'2025-03-10 10:27:43.095526',2,3,2,1,'qr');
/*!40000 ALTER TABLE `sim` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `supplier`
--

DROP TABLE IF EXISTS `supplier`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `supplier` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `status` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `phone_number` (`phone_number`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `supplier`
--

LOCK TABLES `supplier` WRITE;
/*!40000 ALTER TABLE `supplier` DISABLE KEYS */;
INSERT INTO `supplier` VALUES (1,'Vinaphone Center','0486235791','supportbussiness@vinaphone.com','số 57 Huỳnh Thúc Kháng, P. Láng Hạ, Q. Đống Đa, TP. Hà Nội',1),(2,'Mobifone Center','0197648536','supportbussiness@mobifone.com','182-184, Đường Lê Lợi, Khóm. Châu Quới,  P. Châu Phú B, Tp. Châu Đốc, tỉnh An Giang',0),(3,'Viettel Center','0123586497','supportbussiness@viettel.com','Lô D26, Khu đô thị mới Cầu Giấy, phường Yên Hòa, quận Cầu Giấy, Hà Nội',1),(4,'Vietnammobile Company','06452452635','bussinesscenter@vnmobile.com','98 Tôn Thất Tùng, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh',1),(5,'Gmobile Company','04831956894','bussinesscenter@gmobile.com','280B Lạc Long Quân, Quận Tây Hồ, Thành phố Hà Nội',0);
/*!40000 ALTER TABLE `supplier` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_blacklistedtoken`
--

DROP TABLE IF EXISTS `token_blacklist_blacklistedtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_blacklistedtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `blacklisted_at` datetime(6) NOT NULL,
  `token_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_id` (`token_id`),
  CONSTRAINT `token_blacklist_blacklistedtoken_token_id_3cc7fe56_fk` FOREIGN KEY (`token_id`) REFERENCES `token_blacklist_outstandingtoken` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_blacklistedtoken`
--

LOCK TABLES `token_blacklist_blacklistedtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_blacklistedtoken` VALUES (1,'2025-03-07 11:32:01.840382',2);
/*!40000 ALTER TABLE `token_blacklist_blacklistedtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token_blacklist_outstandingtoken`
--

DROP TABLE IF EXISTS `token_blacklist_outstandingtoken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `token_blacklist_outstandingtoken` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` longtext NOT NULL,
  `created_at` datetime(6) DEFAULT NULL,
  `expires_at` datetime(6) NOT NULL,
  `user_id` bigint DEFAULT NULL,
  `jti` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `token_blacklist_outstandingtoken_jti_hex_d9bdf6f7_uniq` (`jti`),
  KEY `token_blacklist_outstandingtoken_user_id_83bc629a_fk_account_id` (`user_id`),
  CONSTRAINT `token_blacklist_outstandingtoken_user_id_83bc629a_fk_account_id` FOREIGN KEY (`user_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token_blacklist_outstandingtoken`
--

LOCK TABLES `token_blacklist_outstandingtoken` WRITE;
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` DISABLE KEYS */;
INSERT INTO `token_blacklist_outstandingtoken` VALUES (1,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTkyNjEyNCwiaWF0IjoxNzQxMzIxMzI0LCJqdGkiOiJlZDAzMWVlNjk1ZDQ0NGRhYTJiNjg4NDE2NWM0ZWYyMiIsInVzZXJfaWQiOjZ9.fkC2-CtW3Ukx_Jg1odEeYT3icp0TP8rd0aa1m-t_IDs','2025-03-07 04:22:04.735225','2025-03-14 04:22:04.000000',6,'ed031ee695d444daa2b6884165c4ef22'),(2,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTkyNjIzOCwiaWF0IjoxNzQxMzIxNDM4LCJqdGkiOiIxMDBmOWI1NTRkOTQ0N2M0YWJjNDUxY2JlZDViZTZkYyIsInVzZXJfaWQiOjZ9.kfaz99qjXZ171DEi4no1HsHgU2tY6bw-3ga-rLMOPbs','2025-03-07 04:23:58.167923','2025-03-14 04:23:58.000000',6,'100f9b554d9447c4abc451cbed5be6dc'),(3,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MTkyNjQ0OCwiaWF0IjoxNzQxMzIxNjQ4LCJqdGkiOiI3ZWM1ZjRkODViNjk0ZDgwYTliNGM3MTc4ZTYyNTBjZSIsInVzZXJfaWQiOjZ9.lY73T4aJGmKFK-Pytr7SJoef0TIbq_vqEUSzHGo5yaQ','2025-03-07 04:27:28.680311','2025-03-14 04:27:28.000000',6,'7ec5f4d85b694d80a9b4c7178e6250ce'),(4,'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0MjQ2MjI3MywiaWF0IjoxNzQxODU3NDczLCJqdGkiOiI5NjBhYzI2OTQwZTg0NDIzYmExZTIyODg3MThmZmI5ZiIsInVzZXJfaWQiOjF9.YLpLHVmElTlKAR2z6-wYPdLC4Wu0eX2PpXSOERYZock','2025-03-13 09:17:53.421148','2025-03-20 09:17:53.000000',1,'960ac26940e84423ba1e2288718ffb9f');
/*!40000 ALTER TABLE `token_blacklist_outstandingtoken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ward`
--

DROP TABLE IF EXISTS `ward`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ward` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL,
  `district_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ward_district_id_5f868993_fk_district_id` (`district_id`),
  CONSTRAINT `ward_district_id_5f868993_fk_district_id` FOREIGN KEY (`district_id`) REFERENCES `district` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ward`
--

LOCK TABLES `ward` WRITE;
/*!40000 ALTER TABLE `ward` DISABLE KEYS */;
INSERT INTO `ward` VALUES (1,'Phường Bến Nghé',1),(2,'Phường Bến Thành',1),(3,'Phường Nguyễn Thái Bình',1),(4,'Phường Cô Giang',1),(5,'Phường Võ Thị Sáu',2),(6,'Phường 7',2),(7,'Phường 8',2),(8,'Phường 9',2),(9,'Phường 10',2),(10,'Phường 11',2),(11,'Phường 12',2),(12,'Phường 13',2),(13,'Phường 1',3),(14,'Phường 2',3),(15,'Phường 3',3),(16,'Phường 4',3),(17,'Phường 5',3),(18,'Phường 6',3),(19,'Phường 7',3),(20,'Phường 8',3),(21,'Phường 9',3),(22,'Phường 10',3),(23,'Phường 11',3),(24,'Phường 12',3),(25,'Phường An Hải Bắc',25),(26,'Phường An Hải Tây',25),(27,'Phường Nại Hiên Đông',25),(28,'Phường Thọ Quang',25),(29,'Phường Hòa Cường Bắc',23),(30,'Phường Hòa Cường Nam',23),(31,'Phường Bình Thuận',23),(32,'Phường Hải Châu I',23),(33,'Phường Hải Châu II',23),(34,'Phường Thanh Bình',23),(35,'Phường Vĩnh Trung',24),(36,'Phường Tân Chính',24),(37,'Phường Chính Gián',24),(38,'Phường Thạc Gián',24),(39,'Phường An Khê',24),(40,'Phường Hòa Khê',24),(41,'Phường Hòa Hiệp Nam',27),(42,'Phường Hòa Hiệp Bắc',27),(43,'Phường Hòa Khánh Bắc',27),(44,'Phường Hòa Khánh Nam',27),(45,'Phường Hòa Minh',27),(46,'Phường An Hòa',61),(47,'Phường An Nghiệp',61),(48,'Phường Cái Khế',61),(49,'Phường Xuân Khánh',61),(50,'Phường Thới Bình',61),(51,'Phường Trà An',62),(52,'Phường Trà Nóc',62),(53,'Phường Thới Hòa',62),(54,'Phường Hưng Phú',62);
/*!40000 ALTER TABLE `ward` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-03-15 16:42:01
