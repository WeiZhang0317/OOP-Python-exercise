-- MySQL dump 10.13  Distrib 8.0.23, for Win64 (x86_64)
--
-- Host: localhost    Database: fresh_harvest12
-- ------------------------------------------------------
-- Server version	8.0.23

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
-- Table structure for table `corporate_customers`
--

DROP TABLE IF EXISTS `corporate_customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corporate_customers` (
  `cust_id` int NOT NULL,
  `discount_rate` float DEFAULT NULL,
  `max_credit` float DEFAULT NULL,
  `min_balance` float DEFAULT NULL,
  PRIMARY KEY (`cust_id`),
  CONSTRAINT `corporate_customers_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `customers` (`cust_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corporate_customers`
--

LOCK TABLES `corporate_customers` WRITE;
/*!40000 ALTER TABLE `corporate_customers` DISABLE KEYS */;
INSERT INTO `corporate_customers` VALUES (25,0.15,2000,500),(26,0.12,3000,700),(27,0.2,4000,800),(28,0.18,5000,1000);
/*!40000 ALTER TABLE `corporate_customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `credit_card_payments`
--

DROP TABLE IF EXISTS `credit_card_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `credit_card_payments` (
  `id` int NOT NULL,
  `card_number` varchar(16) NOT NULL,
  `card_type` varchar(20) NOT NULL,
  `card_expiry_date` varchar(7) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `credit_card_payments_ibfk_1` FOREIGN KEY (`id`) REFERENCES `payments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `credit_card_payments`
--

LOCK TABLES `credit_card_payments` WRITE;
/*!40000 ALTER TABLE `credit_card_payments` DISABLE KEYS */;
INSERT INTO `credit_card_payments` VALUES (8,'1234567812345678','Visa','12/25'),(11,'9876543212345678','MasterCard','11/26');
/*!40000 ALTER TABLE `credit_card_payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customers` (
  `cust_id` int NOT NULL,
  `cust_address` varchar(100) NOT NULL,
  `cust_balance` float DEFAULT NULL,
  `max_owing` float DEFAULT NULL,
  PRIMARY KEY (`cust_id`),
  CONSTRAINT `customers_ibfk_1` FOREIGN KEY (`cust_id`) REFERENCES `persons` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (21,'123 Main St',50,100),(22,'456 Oak Ave',150,100),(23,'789 Maple St',70,100),(24,'987 Cedar St',200,100),(25,'789 Pine Rd',600,100),(26,'101 Maple Blvd',800,100),(27,'789 Oak St',900,100),(28,'987 Birch St',1200,100);
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `debit_card_payments`
--

DROP TABLE IF EXISTS `debit_card_payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `debit_card_payments` (
  `id` int NOT NULL,
  `bank_name` varchar(50) NOT NULL,
  `debit_card_number` varchar(16) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `debit_card_payments_ibfk_1` FOREIGN KEY (`id`) REFERENCES `payments` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `debit_card_payments`
--

LOCK TABLES `debit_card_payments` WRITE;
/*!40000 ALTER TABLE `debit_card_payments` DISABLE KEYS */;
INSERT INTO `debit_card_payments` VALUES (9,'ABC Bank','8765432187654321'),(12,'XYZ Bank','1234567812348765');
/*!40000 ALTER TABLE `debit_card_payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `id` int NOT NULL AUTO_INCREMENT,
  `item_id` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `inventory_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,1,50),(2,2,30),(3,3,40),(4,4,20),(5,5,60),(6,6,35),(7,7,25),(8,8,15),(9,9,45),(10,10,40),(11,11,10),(12,12,8),(13,13,50),(14,14,30),(15,15,40),(16,16,20),(17,17,60),(18,18,35),(19,19,25),(20,20,15),(21,21,45),(22,22,40),(23,23,10),(24,24,8);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `price` float NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'Carrot',2),(2,'Spinach',3),(3,'Broccoli',4),(4,'Lettuce',3.5),(5,'Potato',1.5),(6,'Sweet Potato',5),(7,'Tomato Pack',5),(8,'Pepper Pack',8),(9,'Cucumber',0.8),(10,'Eggplant',3),(11,'Veggie Box',20),(12,'Large Veggie Box',30),(13,'Carrot',2),(14,'Spinach',3),(15,'Broccoli',4),(16,'Lettuce',3.5),(17,'Potato',1.5),(18,'Sweet Potato',5),(19,'Tomato Pack',5),(20,'Pepper Pack',8),(21,'Cucumber',0.8),(22,'Eggplant',3),(23,'Veggie Box',20),(24,'Large Veggie Box',30);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_lines`
--

DROP TABLE IF EXISTS `order_lines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_lines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_id` int DEFAULT NULL,
  `item_id` int DEFAULT NULL,
  `quantity` int NOT NULL,
  `line_total` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `order_id` (`order_id`),
  KEY `item_id` (`item_id`),
  CONSTRAINT `order_lines_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  CONSTRAINT `order_lines_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_lines`
--

LOCK TABLES `order_lines` WRITE;
/*!40000 ALTER TABLE `order_lines` DISABLE KEYS */;
INSERT INTO `order_lines` VALUES (5,5,13,2,4),(6,6,19,1,5),(7,7,15,3,12),(8,8,24,1,30);
/*!40000 ALTER TABLE `order_lines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `orders`
--

DROP TABLE IF EXISTS `orders`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `orders` (
  `id` int NOT NULL AUTO_INCREMENT,
  `order_number` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  `order_status` varchar(50) NOT NULL,
  `total_cost` float NOT NULL,
  `staff_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_number` (`order_number`),
  KEY `customer_id` (`customer_id`),
  KEY `staff_id` (`staff_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`cust_id`),
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`staff_id`) REFERENCES `staff` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `orders`
--

LOCK TABLES `orders` WRITE;
/*!40000 ALTER TABLE `orders` DISABLE KEYS */;
INSERT INTO `orders` VALUES (5,1001,21,'2024-10-17 23:39:10','Pending',200,29),(6,1002,22,'2024-10-17 23:39:10','Shipped',150,30),(7,1003,23,'2024-10-17 23:39:10','Pending',100,31),(8,1004,24,'2024-10-17 23:39:10','Shipped',200,32);
/*!40000 ALTER TABLE `orders` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pack_veggie`
--

DROP TABLE IF EXISTS `pack_veggie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pack_veggie` (
  `id` int NOT NULL,
  `num_of_pack` int NOT NULL,
  `price_per_pack` float NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `pack_veggie_ibfk_1` FOREIGN KEY (`id`) REFERENCES `veggie` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pack_veggie`
--

LOCK TABLES `pack_veggie` WRITE;
/*!40000 ALTER TABLE `pack_veggie` DISABLE KEYS */;
INSERT INTO `pack_veggie` VALUES (19,1,5),(20,2,4);
/*!40000 ALTER TABLE `pack_veggie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `payment_amount` float NOT NULL,
  `payment_date` datetime DEFAULT NULL,
  `customer_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `customer_id` (`customer_id`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`cust_id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (7,45,'2024-10-17 23:39:10',21),(8,100,'2024-10-17 23:39:10',22),(9,200,'2024-10-17 23:39:10',25),(10,75,'2024-10-17 23:39:10',23),(11,150,'2024-10-17 23:39:10',24),(12,250,'2024-10-17 23:39:10',27);
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `persons`
--

DROP TABLE IF EXISTS `persons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `persons` (
  `id` int NOT NULL AUTO_INCREMENT,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `_Person__password` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  KEY `ix_persons_id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `persons`
--

LOCK TABLES `persons` WRITE;
/*!40000 ALTER TABLE `persons` DISABLE KEYS */;
INSERT INTO `persons` VALUES (17,'John','Doe','johndoe','scrypt:32768:8:1$sm81UDOwQzgHzRx6$324f061c5a046124289d078a744406ab5d6c2d556caf0632fffa7062f036569272b0bdccc9a8f7c982346b149dd07360d7d479083cd9d8566baaa0d2ad1547b1'),(18,'Jane','Smith','janesmith','scrypt:32768:8:1$5GOU76Jd7g5URaoR$2ca967783c9648e522eab86063ec045336d48f27f72a0c2e0a92c5acc755945f49117ec3858050cfc0193768c3517587e90f50fd109a0b00eb4aa6e43761ee18'),(19,'John','Smith','johnsmith','scrypt:32768:8:1$7o8Vextjfr8isTIp$8665125e8d56f44f49b310ff1e488d423a591bbcdb5db4efcf9282b618d7d91f395984cc31e75f45ef6ed82f8c9dc354944d1ffb9aef1561dd690f061e7c77b9'),(20,'Linda','Brown','lindabrown','scrypt:32768:8:1$728KwdruqpYZ6oxG$19bc73333b5e779702f7b327d2ee65e87d2d1076baa051af7a69e3b37e1c51192b7c25cba1b1164d1009227219108a3a6e9b646e1759ffd50adb7212c126fdfa'),(21,'Mike','Johnson','mikejohnson','scrypt:32768:8:1$2lfN1A0HXv5pbGc5$d4479f75779ac30630a9f75bae69974e0a2a3707b37f64e205964aa20909eaf6f586b26ae2c60b6b4d4d33769853ff0a51b2a663154acc4ba14a07107d370276'),(22,'Lucy','Brown','lucybrown','scrypt:32768:8:1$6Ra0YnJSZbBOYeMT$cc3a088432757895a7f6c20550eebe37ceebd8271c9a2bb6248a108597e889e6e30de1c85b3f8e848db3b2b231a123526c0a3d42c5d51c2f0ba56e7a2974bba5'),(23,'John','Smith','johnsmithcustomer','scrypt:32768:8:1$rG6kW6MWcpbaZsAS$c398a541d73aad6ac3ed9c32302e76642fd63d289ae938e75b4ecb5f320fcc7245fb30072e9ac444099971eea33ba96e09f2c45da2ac22810eb3fb5d5ea0c2a4'),(24,'Linda','Brown','lindabrowncustomer','scrypt:32768:8:1$RYuX7GE5RJOIXpz0$b7d60ce68730a328929a0d885f5f120c69a9fe8f1004b13e5defa9b89a9edf3becee7c22d7d5c1b49cfebbf08d5bf541a8d261c9b32caf8ca8cb5ca4398a033f'),(25,'George','Williams','georgewilliams','scrypt:32768:8:1$c1HVK5so1sCQtG78$f924e7599a48fce1302aa250e93cf96e054bfa72e438d7ff666fa01e300490f16dc27aedd2cc2b6d665ff14e628c9092b7b16066055122fa314132f425e8b299'),(26,'Emma','Green','emmagreen','scrypt:32768:8:1$usVpnFFmVAPQm9B9$723016cfdeb099b1b78ca09c5712df99bc518bc8ddd83660948d1d1e67b3ca3bef75c3c77201766b2fe27ccf992b89f92d7afd5e1a0353bd246b0e746f8b7a27'),(27,'Michael','Johnson','michaeljohnson','scrypt:32768:8:1$L7BquXsnEPOe448s$b7347f2748b6f34b974e910c32278c5644d86ba91e3a4265a3e91bec144d6f59f5987e903f07cbc40d4a8ad3afe14e9389bd53ac568b8d2be765c1a8bfe3a75d'),(28,'Susan','Green','susangreen','scrypt:32768:8:1$YdPedxGL9ttwqerR$25608e432fc0ad3130ca846f398628742a611b8b23ed87f821f608cf350a911fa441dea14f8573f310e5360cee62af9c2264e2df816bef0894bf74486b74924a'),(29,'Alice','Williams','alicewilliams','scrypt:32768:8:1$IBrxtw6JGNvrzcnU$73a56180affb1dbe7305bb5123d9d856948d525cb475e7f52aeeb142414930cb248af5e4164ee54c64468cab11d8dee27cd4ce26c0d1fe2ee584a547456b542a'),(30,'Bob','Taylor','bobtaylor','scrypt:32768:8:1$qMkbQjWg6OLnqshI$05f311311f949f0ad79a14833c6c02faaad9ada17f49afab0d16fb9efac32983ba18c9e34af8a1aefeb70103127ec6143ffc0e26beb4b3b9c2db049534a56cc2'),(31,'Jake','Black','jakeblack','scrypt:32768:8:1$7Oxf3Iuujz1G5Z4v$ab7f604526500557891dc42e31a21557b67fcc72c6252a61d94e5efe05c55a706d4229b21bf4b26faaa7b3b5630f37c3edb403a7ec117b4966854c2883d86f61'),(32,'Alice','Green','alicegreen','scrypt:32768:8:1$ANLRQORQoXW8OTKU$5640cf7b15e7a32dceeb938ebe90e5a6009f9fd38335b89c0cd41849e143da6059ab084ca718d470e0213cc4df1f3ccca2e8d490dd662e466627e581bf967116');
/*!40000 ALTER TABLE `persons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `premade_boxes`
--

DROP TABLE IF EXISTS `premade_boxes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `premade_boxes` (
  `id` int NOT NULL,
  `box_size` varchar(20) NOT NULL,
  `num_of_boxes` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `premade_boxes_ibfk_1` FOREIGN KEY (`id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `premade_boxes`
--

LOCK TABLES `premade_boxes` WRITE;
/*!40000 ALTER TABLE `premade_boxes` DISABLE KEYS */;
INSERT INTO `premade_boxes` VALUES (23,'Medium',1),(24,'Large',2);
/*!40000 ALTER TABLE `premade_boxes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `id` int NOT NULL,
  `date_joined` datetime DEFAULT NULL,
  `dept_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`id`) REFERENCES `persons` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (29,'2024-10-17 23:39:10','Sales'),(30,'2024-10-17 23:39:10','Logistics'),(31,'2024-10-17 23:39:10','HR'),(32,'2024-10-17 23:39:10','Marketing');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `unit_price_veggie`
--

DROP TABLE IF EXISTS `unit_price_veggie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `unit_price_veggie` (
  `id` int NOT NULL,
  `price_per_unit` float NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `unit_price_veggie_ibfk_1` FOREIGN KEY (`id`) REFERENCES `veggie` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `unit_price_veggie`
--

LOCK TABLES `unit_price_veggie` WRITE;
/*!40000 ALTER TABLE `unit_price_veggie` DISABLE KEYS */;
INSERT INTO `unit_price_veggie` VALUES (21,0.8,5),(22,1.5,2);
/*!40000 ALTER TABLE `unit_price_veggie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `veggie`
--

DROP TABLE IF EXISTS `veggie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `veggie` (
  `id` int NOT NULL,
  `veg_name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `veggie_ibfk_1` FOREIGN KEY (`id`) REFERENCES `items` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `veggie`
--

LOCK TABLES `veggie` WRITE;
/*!40000 ALTER TABLE `veggie` DISABLE KEYS */;
INSERT INTO `veggie` VALUES (13,'Carrot'),(14,'Spinach'),(15,'Broccoli'),(16,'Lettuce'),(17,'Potato'),(18,'Sweet Potato'),(19,'Tomato'),(20,'Pepper'),(21,'Cucumber'),(22,'Eggplant');
/*!40000 ALTER TABLE `veggie` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `weighted_veggie`
--

DROP TABLE IF EXISTS `weighted_veggie`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `weighted_veggie` (
  `id` int NOT NULL,
  `weight` float NOT NULL,
  `weight_per_kilo` float NOT NULL,
  PRIMARY KEY (`id`),
  CONSTRAINT `weighted_veggie_ibfk_1` FOREIGN KEY (`id`) REFERENCES `veggie` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `weighted_veggie`
--

LOCK TABLES `weighted_veggie` WRITE;
/*!40000 ALTER TABLE `weighted_veggie` DISABLE KEYS */;
INSERT INTO `weighted_veggie` VALUES (17,2,1.5),(18,2.5,2);
/*!40000 ALTER TABLE `weighted_veggie` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-10-18  0:17:01
