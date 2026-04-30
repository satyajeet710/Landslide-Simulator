-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 04, 2026 at 08:45 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `linearsmart`
--

-- --------------------------------------------------------

--
-- Table structure for table `death_images`
--

CREATE TABLE `death_images` (
  `sno` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `image_source` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `death_images`
--

INSERT INTO `death_images` (`sno`, `scenario_id`, `image_source`) VALUES
(3, 2, 'death_images\\death1.jpg'),
(4, 2, 'death_images\\death2.jpg'),
(5, 3, 'death_images\\death1.jpg'),
(6, 3, 'death_images\\death2.jpg'),
(7, 6, 'death_images\\death1.jpg'),
(8, 6, 'death_images\\death2.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `demographic`
--

CREATE TABLE `demographic` (
  `sno` int(11) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `id` varchar(24) NOT NULL,
  `Age` int(2) NOT NULL,
  `Gender` varchar(2) NOT NULL,
  `Education` varchar(32) NOT NULL,
  `Major` varchar(32) NOT NULL,
  `Occupation` varchar(32) NOT NULL,
  `Email` varchar(1024) NOT NULL,
  `city_belong_to` varchar(300) NOT NULL,
  `liveno_currently_live` varchar(300) NOT NULL,
  `live_long` varchar(300) NOT NULL,
  `livereason` varchar(1000) NOT NULL,
  `dwell_type` varchar(300) NOT NULL,
  `household_size` varchar(300) NOT NULL,
  `owner` varchar(300) NOT NULL,
  `source_of_income` varchar(300) NOT NULL,
  `income` varchar(300) NOT NULL,
  `knowledge` varchar(300) NOT NULL,
  `inslp` varchar(300) NOT NULL,
  `inspur` varchar(300) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `demographic`
--

INSERT INTO `demographic` (`sno`, `Timestamp`, `id`, `Age`, `Gender`, `Education`, `Major`, `Occupation`, `Email`, `city_belong_to`, `liveno_currently_live`, `live_long`, `livereason`, `dwell_type`, `household_size`, `owner`, `source_of_income`, `income`, `knowledge`, `inslp`, `inspur`) VALUES
(1, '2025-12-12 10:01:29', '693be7cac8b606.23870600', 45, 'M', 'Intermediate', 'dffgf', 'dff', 'ds@gmail.com', 'fe', 'yes', '1-5 Years', 'NULL', 'Formal Building', '3-6 members', 'NULL', 'fill-in', '5,000 - 25,000', 'Basic understanding', '', ''),
(2, '2025-12-15 06:44:58', '693fad611bcdb2.23095702', 43, 'M', 'Intermediate', 'B.A.', 'Govt. Job Police', 'CS-05@gmail.com', 'Mandi', 'yes', '5-10 Years', 'NULL', 'Formal Building', '3-6 members', 'NULL', 'Government Job', '50,000 - 75,000', 'Basic understanding', '', '');

-- --------------------------------------------------------

--
-- Table structure for table `game`
--

CREATE TABLE `game` (
  `consent` varchar(6) NOT NULL DEFAULT 'false',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `sno` int(11) NOT NULL,
  `id` varchar(24) NOT NULL,
  `day` int(3) NOT NULL,
  `invest` float NOT NULL DEFAULT 0,
  `hinsur` float NOT NULL DEFAULT 0,
  `linsur` float NOT NULL DEFAULT 0,
  `pinsur` float NOT NULL DEFAULT 0,
  `cumulative_invest` float NOT NULL DEFAULT 0,
  `weight_invest` float NOT NULL,
  `time_span` int(3) NOT NULL DEFAULT 60,
  `daily_income` float NOT NULL DEFAULT 10,
  `return_mitigation` float NOT NULL DEFAULT 0.99,
  `dampening_factor_investment` float NOT NULL,
  `p_property` float NOT NULL DEFAULT 0.40606,
  `rand_property` float DEFAULT NULL,
  `p_fatality` float NOT NULL DEFAULT 0.77575,
  `rand_fatality` float DEFAULT NULL,
  `p_injury` float NOT NULL DEFAULT 0.36718,
  `rand_injury` float DEFAULT NULL,
  `p_temporal` float DEFAULT NULL,
  `rand_spatial` float NOT NULL,
  `p_spatial` float NOT NULL DEFAULT 0.9,
  `p_rain` float DEFAULT NULL,
  `p_investment` float DEFAULT NULL,
  `p_landslide` float DEFAULT NULL,
  `landslide_threshold` float DEFAULT NULL,
  `landslide` int(2) DEFAULT NULL,
  `fatality_daily_inc_loss` float NOT NULL,
  `damage_fatality` int(2) DEFAULT NULL,
  `injury_daily_inc_loss` float NOT NULL,
  `damage_injury` int(2) DEFAULT NULL,
  `wealth_property` float NOT NULL,
  `damage_property` int(2) DEFAULT NULL,
  `money_ini` float NOT NULL DEFAULT 100,
  `damage` float DEFAULT NULL,
  `net_money` float DEFAULT NULL,
  `final_money` int(11) DEFAULT NULL,
  `day_initial_temporal` int(11) NOT NULL DEFAULT 1,
  `invest-retaining_walls` decimal(12,2) DEFAULT NULL,
  `invest-drainage_systems` decimal(12,2) DEFAULT NULL,
  `invest-land_use_planning` decimal(12,2) DEFAULT NULL,
  `invest-soil_classification` decimal(12,2) DEFAULT NULL,
  `invest-tree_planting` decimal(12,2) DEFAULT NULL,
  `invest-water_management` decimal(12,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `game`
--

INSERT INTO `game` (`consent`, `timestamp`, `sno`, `id`, `day`, `invest`, `hinsur`, `linsur`, `pinsur`, `cumulative_invest`, `weight_invest`, `time_span`, `daily_income`, `return_mitigation`, `dampening_factor_investment`, `p_property`, `rand_property`, `p_fatality`, `rand_fatality`, `p_injury`, `rand_injury`, `p_temporal`, `rand_spatial`, `p_spatial`, `p_rain`, `p_investment`, `p_landslide`, `landslide_threshold`, `landslide`, `fatality_daily_inc_loss`, `damage_fatality`, `injury_daily_inc_loss`, `damage_injury`, `wealth_property`, `damage_property`, `money_ini`, `damage`, `net_money`, `final_money`, `day_initial_temporal`, `invest-retaining_walls`, `invest-drainage_systems`, `invest-land_use_planning`, `invest-soil_classification`, `invest-tree_planting`, `invest-water_management`) VALUES
('true', '2025-12-12 10:01:29', 1, '693be7cac8b606.23870600', 0, 0, 0, 0, 0, 0, 0.7, 20, 8760, 0.84, 1, 0.3, NULL, 0.09, NULL, 0.9, NULL, NULL, 0.88, 0.85638, NULL, NULL, NULL, NULL, NULL, 0.5, NULL, 0.25, NULL, 0.5, NULL, 5000000, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:01:46', 2, '693be7cac8b606.23870600', 1, 1800, 0, 488, 0, 1800, 0.7, 20, 8760, 0.84, 1, 0.3, 0.63747, 0.09, 0.84535, 0.9, 0.36362, 0.088411, 0, 0.85638, 0.0757134, 0.569208, 0.42116, 0.58186, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 6472, 5006472, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:01:56', 3, '693be7cac8b606.23870600', 2, 0, 1173, 488, 1884, 1800, 0.7, 20, 8760, 0.84, 1, 0.3, 0.36887, 0.09, 0.67955, 0.9, 0.98, 0.062823, 0, 0.85638, 0.0538004, 0.746289, 0.538542, 0.28233, 1, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 5215, 5011687, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:02:07', 4, '693be7cac8b606.23870600', 3, 444, 0, 0, 0, 2244, 0.7, 20, 8760, 0.84, 1, 0.3, 0.25756, 0.09, 0.89317, 0.9, 0.25035, 0.064422, 0, 0.85638, 0.0551697, 0.782998, 0.56465, 0.65597, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 8316, 5020003, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:02:20', 5, '693be7cac8b606.23870600', 4, 8000, 0, 0, 0, 10244, 0.7, 20, 8760, 0.84, 1, 0.3, 0.19591, 0.09, 0.97433, 0.9, 0.94681, 0.059965, 0, 0.85638, 0.0513528, 0.461923, 0.338752, 0.49532, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 760, 5020763, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:02:36', 6, '693be7cac8b606.23870600', 5, 0, 1173, 488, 1884, 10244, 0.7, 20, 8760, 0.84, 1, 0.3, 0.67073, 0.09, 0.80304, 0.9, 0.86846, 0.218549, 0, 0.85638, 0.187161, 0.530487, 0.427489, 0.28374, 1, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 5215, 5025978, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:02:45', 7, '693be7cac8b606.23870600', 6, 8000, 0, 0, 0, 18244, 0.7, 20, 8760, 0.84, 1, 0.3, 0.64589, 0.09, 0.27176, 0.9, 0.91166, 0.674991, 0, 0.85638, 0.578049, 0.409267, 0.459901, 0.50201, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 760, 5026738, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:02:55', 8, '693be7cac8b606.23870600', 7, 8000, 0, 0, 0, 26244, 0.7, 20, 8760, 0.84, 1, 0.3, 0.17033, 0.09, 0.52511, 0.9, 0.53745, 0.878744, 0, 0.85638, 0.752539, 0.347815, 0.469232, 0.12301, 1, 0.5, 0, 0.25, 1, 0.5, 1, 5000000, 2500000, -2501430, 2525308, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:03:05', 9, '693be7cac8b606.23870600', 8, 6000, 0, 0, 0, 32244, 0.7, 20, 6570, 0.84, 1, 0.3, 0.13409, 0.09, 0.19378, 0.9, 0.33017, 0.332772, 0, 0.85638, 0.284979, 0.319349, 0.309038, 0.45636, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 570, 2525878, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:03:13', 10, '693be7cac8b606.23870600', 9, 6000, 0, 0, 0, 38244, 0.7, 20, 6570, 0.84, 1, 0.3, 0.73076, 0.09, 0.62464, 0.9, 0.27229, 0.043983, 0, 0.85638, 0.0376662, 0.299176, 0.220723, 0.75789, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 570, 2526448, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:03:23', 11, '693be7cac8b606.23870600', 10, 6000, 0, 0, 0, 44244, 0.7, 20, 6570, 0.84, 1, 0.3, 0.51516, 0.09, 0.92466, 0.9, 0.09885, 0.024852, 0, 0.85638, 0.0212828, 0.284254, 0.205363, 0.86256, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 570, 2527018, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:03:35', 12, '693be7cac8b606.23870600', 11, 900, 0, 0, 0, 45144, 0.7, 20, 6570, 0.84, 1, 0.3, 0.61685, 0.09, 0.67957, 0.9, 0.20405, 0.032376, 0, 0.85638, 0.0277262, 0.298338, 0.217155, 0.08377, 1, 0.5, 0, 0.25, 1, 0.5, 0, 2500000, 0, 4027.5, 2531046, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:03:44', 13, '693be7cac8b606.23870600', 12, 4500, 0, 0, 0, 49644, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.89065, 0.09, 0.74558, 0.9, 0.57585, 0.084888, 0, 0.85638, 0.0726964, 0.28845, 0.223724, 0.75787, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 427.5, 2531473, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:03:55', 14, '693be7cac8b606.23870600', 13, 4800, 0, 0, 0, 54444, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.40173, 0.09, 0.29183, 0.9, 0.57676, 0.088411, 0, 0.85638, 0.0757134, 0.278878, 0.217929, 0.96443, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 127.5, 2531601, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:04:05', 15, '693be7cac8b606.23870600', 14, 4500, 0, 0, 0, 58944, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.4713, 0.09, 0.91577, 0.9, 0.65243, 0.062823, 0, 0.85638, 0.0538004, 0.271986, 0.20653, 0.81334, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 427.5, 2532028, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:04:18', 16, '693be7cac8b606.23870600', 15, 4500, 0, 0, 0, 63444, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.9107, 0.09, 0.71621, 0.9, 0.96273, 0.064422, 0, 0.85638, 0.0551697, 0.266073, 0.202802, 0.6182, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 427.5, 2532456, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:04:28', 17, '693be7cac8b606.23870600', 16, 4500, 0, 0, 0, 67944, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.15666, 0.09, 0.85988, 0.9, 0.44784, 0.059965, 0, 0.85638, 0.0513528, 0.260952, 0.198072, 0.68274, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 427.5, 2532883, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:04:37', 18, '693be7cac8b606.23870600', 17, 560, 0, 0, 0, 68504, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.08378, 0.09, 0.22959, 0.9, 0.23463, 0.218549, 0, 0.85638, 0.187161, 0.26853, 0.244119, 0.25754, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 4367.5, 2537251, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:04:50', 19, '693be7cac8b606.23870600', 18, 1100, 0, 0, 0, 69604, 0.7, 20, 4927.5, 0.84, 1, 0.3, 0.5552, 0.09, 0.25377, 0.9, 0.84873, 0.674991, 0, 0.85638, 0.578049, 0.274215, 0.365365, 0.07004, 1, 0.5, 0, 0.25, 1, 0.5, 0, 2500000, 0, 2595.62, 2539846, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:05:01', 20, '693be7cac8b606.23870600', 19, 222, 0, 0, 0, 69826, 0.7, 20, 3695.62, 0.84, 1, 0.3, 0.11664, 0.09, 0.29196, 0.9, 0.03835, 0.878744, 0, 0.85638, 0.752539, 0.280364, 0.422017, 0.93431, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 3473.62, 2543320, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-12 10:05:10', 21, '693be7cac8b606.23870600', 20, 679, 0, 0, 0, 70505, 0.7, 20, 3695.62, 0.84, 1, 0.3, 0.41582, 0.09, 0.59961, 0.9, 0.6653, 0.332772, 0, 0.85638, 0.284979, 0.284914, 0.284933, 0.227, 1, 0.5, 0, 0.25, 1, 0.5, 0, 2500000, 0, 2092.72, 2545412, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:44:58', 22, '693fad611bcdb2.23095702', 0, 0, 0, 0, 0, 0, 0.7, 20, 8760, 0.84, 1, 0.3, NULL, 0.09, NULL, 0.9, NULL, NULL, 0.72, 0.54788, NULL, NULL, NULL, NULL, NULL, 0.5, NULL, 0.25, NULL, 0.5, NULL, 5000000, NULL, NULL, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:45:36', 23, '693fad611bcdb2.23095702', 1, 6000, 0, 0, 1884, 6000, 0.7, 20, 8760, 0.84, 1, 0.3, 0.29763, 0.09, 0.99347, 0.9, 0.35298, 0.088411, 0, 0.54788, 0.0484386, 0.236412, 0.18002, 0.41454, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 876, 5000876, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:46:18', 24, '693fad611bcdb2.23095702', 2, 4500, 0, 0, 1884, 10500, 0.7, 20, 8760, 0.84, 1, 0.3, 0.99926, 0.09, 0.47649, 0.9, 0.75343, 0.062823, 0, 0.54788, 0.0344195, 0.26311, 0.194503, 0.15766, 1, 0.5, 0, 0.25, 1, 0.5, 0, 5000000, 0, 186, 5001062, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:46:57', 25, '693fad611bcdb2.23095702', 3, 5500, 0, 488, 1884, 16000, 0.7, 20, 6570, 0.84, 1, 0.3, 0.10715, 0.09, 0.84808, 0.9, 0.78286, 0.064422, 0, 0.54788, 0.0352955, 0.24217, 0.180107, 0.39236, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, -1302, 4999760, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:47:27', 26, '693fad611bcdb2.23095702', 4, 2000, 0, 0, 1884, 18000, 0.7, 20, 6570, 0.84, 1, 0.3, 0.13709, 0.09, 0.77591, 0.9, 0.33128, 0.059965, 0, 0.54788, 0.0328536, 0.26762, 0.19719, 0.8872, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 2686, 5002446, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:47:39', 27, '693fad611bcdb2.23095702', 5, 2000, 0, 0, 0, 20000, 0.7, 20, 6570, 0.84, 1, 0.3, 0.89363, 0.09, 0.58044, 0.9, 0.37511, 0.218549, 0, 0.54788, 0.119739, 0.28815, 0.237626, 0.46733, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 4570, 5007016, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:48:02', 28, '693fad611bcdb2.23095702', 6, 2000, 0, 0, 1884, 22000, 0.7, 20, 6570, 0.84, 1, 0.3, 0.39232, 0.09, 0.0714, 0.9, 0.08697, 0.674991, 0, 0.54788, 0.369814, 0.304808, 0.32431, 0.05498, 1, 0.5, 1, 0.25, 1, 0.5, 0, 5000000, 0, -1420.25, 5005596, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:48:46', 29, '693fad611bcdb2.23095702', 7, 1700, 0, 0, 0, 23700, 0.7, 20, 2463.75, 0.84, 1, 0.3, 0.37898, 0.09, 0.35488, 0.9, 0.88294, 0.878744, 0, 0.54788, 0.481446, 0.299829, 0.354314, 0.57067, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 763.75, 5006360, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:49:03', 30, '693fad611bcdb2.23095702', 8, 1000, 0, 0, 0, 24700, 0.7, 20, 2463.75, 0.84, 1, 0.3, 0.84324, 0.09, 0.90589, 0.9, 0.3894, 0.332772, 0, 0.54788, 0.182319, 0.302487, 0.266437, 0.00799, 1, 0.5, 0, 0.25, 1, 0.5, 0, 5000000, 0, 847.812, 5007207, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:49:57', 31, '693fad611bcdb2.23095702', 9, 1750, 0, 0, 0, 26450, 0.7, 20, 1847.81, 0.84, 1, 0.3, 0.57058, 0.09, 0.29347, 0.9, 0.04542, 0.043983, 0, 0.54788, 0.0240974, 0.294688, 0.213511, 0.10018, 1, 0.5, 0, 0.25, 1, 0.5, 0, 5000000, 0, -364.141, 5006843, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:50:15', 32, '693fad611bcdb2.23095702', 10, 1000, 0, 0, 0, 27450, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.22129, 0.09, 0.20975, 0.9, 0.62864, 0.024852, 0, 0.54788, 0.0136159, 0.292214, 0.208635, 0.39803, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 385.859, 5007229, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:50:30', 33, '693fad611bcdb2.23095702', 11, 800, 0, 0, 0, 28250, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.30983, 0.09, 0.71576, 0.9, 0.55003, 0.032376, 0, 0.54788, 0.0177382, 0.291627, 0.20946, 0.31971, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 585.859, 5007815, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:50:46', 34, '693fad611bcdb2.23095702', 12, 600, 0, 0, 0, 28850, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.19217, 0.09, 0.23212, 0.9, 0.25986, 0.084888, 0, 0.54788, 0.0465084, 0.292759, 0.218884, 0.72084, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 785.859, 5008601, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:50:59', 35, '693fad611bcdb2.23095702', 13, 600, 0, 0, 0, 29450, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.85018, 0.09, 0.50264, 0.9, 0.97878, 0.088411, 0, 0.54788, 0.0484386, 0.293844, 0.220222, 0.78122, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 785.859, 5009387, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:51:10', 36, '693fad611bcdb2.23095702', 14, 800, 0, 0, 0, 30250, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.04304, 0.09, 0.68588, 0.9, 0.50189, 0.062823, 0, 0.54788, 0.0344195, 0.293252, 0.215603, 0.96673, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 585.859, 5009972, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:51:18', 37, '693fad611bcdb2.23095702', 15, 600, 0, 0, 0, 30850, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.41467, 0.09, 0.47864, 0.9, 0.07704, 0.064422, 0, 0.54788, 0.0352955, 0.294278, 0.216583, 0.53304, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 785.859, 5010758, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:51:26', 38, '693fad611bcdb2.23095702', 16, 500, 0, 0, 0, 31350, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.28572, 0.09, 0.08741, 0.9, 0.25757, 0.059965, 0, 0.54788, 0.0328536, 0.296052, 0.217092, 0.78001, 0, 0.5, 0, 0.25, 0, 0.5, 0, 5000000, 0, 885.859, 5011644, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:52:09', 39, '693fad611bcdb2.23095702', 17, 500, 0, 0, 0, 31850, 0.7, 20, 1385.86, 0.84, 1, 0.3, 0.15462, 0.09, 0.76337, 0.9, 0.6237, 0.218549, 0, 0.54788, 0.119739, 0.297768, 0.244359, 0.16695, 1, 0.5, 0, 0.25, 1, 0.5, 1, 5000000, 2500000, -2499460, 2512184, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:52:26', 40, '693fad611bcdb2.23095702', 18, 500, 0, 0, 0, 32350, 0.7, 20, 1039.39, 0.84, 1, 0.3, 0.52727, 0.09, 0.6858, 0.9, 0.04474, 0.674991, 0, 0.54788, 0.369814, 0.298051, 0.31958, 0.1309, 1, 0.5, 0, 0.25, 1, 0.5, 0, 2500000, 0, 279.546, 2512463, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:52:37', 41, '693fad611bcdb2.23095702', 19, 500, 0, 0, 0, 32850, 0.7, 20, 779.546, 0.84, 1, 0.3, 0.94898, 0.09, 0.17901, 0.9, 0.77881, 0.878744, 0, 0.54788, 0.481446, 0.297309, 0.35255, 0.34776, 1, 0.5, 0, 0.25, 1, 0.5, 0, 2500000, 0, 84.6594, 2512548, 1, NULL, NULL, NULL, NULL, NULL, NULL),
('true', '2025-12-15 06:53:25', 42, '693fad611bcdb2.23095702', 20, 584, 0, 0, 0, 33434, 0.7, 20, 584.659, 0.84, 1, 0.3, 0.86692, 0.09, 0.02819, 0.9, 0.73543, 0.332772, 0, 0.54788, 0.182319, 0.295214, 0.261345, 0.94317, 0, 0.5, 0, 0.25, 0, 0.5, 0, 2500000, 0, 0.659424, 2512548, 1, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `injury_images`
--

CREATE TABLE `injury_images` (
  `sno` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `image_source` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `message_day`
--

CREATE TABLE `message_day` (
  `sno` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `day` int(11) NOT NULL,
  `image_source` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `message_probability`
--

CREATE TABLE `message_probability` (
  `sno` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `from_prob` float NOT NULL,
  `to_prob` float NOT NULL,
  `image_source` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

-- --------------------------------------------------------

--
-- Table structure for table `nbr_pay`
--

CREATE TABLE `nbr_pay` (
  `id` int(11) NOT NULL,
  `day` float DEFAULT NULL,
  `pay` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `nbr_pay`
--

INSERT INTO `nbr_pay` (`id`, `day`, `pay`) VALUES
(1, 1, 153),
(2, 2, 156),
(3, 3, 161),
(4, 4, 166),
(5, 5, 172),
(6, 6, 178),
(7, 7, 183),
(8, 8, 186),
(9, 9, 189),
(10, 10, 195),
(11, 11, 198),
(12, 12, 205),
(13, 13, 208),
(14, 14, 214),
(15, 15, 220),
(16, 16, 222),
(17, 17, 229),
(18, 18, 230),
(19, 19, 238),
(20, 20, 242),
(21, 21, 248),
(22, 22, 248),
(23, 23, 255),
(24, 24, 258),
(25, 25, 265),
(26, 26, 270),
(27, 27, 271),
(28, 28, 276),
(29, 29, 284),
(30, 30, 292);

-- --------------------------------------------------------

--
-- Table structure for table `param`
--

CREATE TABLE `param` (
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `scenario_id` int(11) NOT NULL,
  `comments` varchar(1000) NOT NULL,
  `weight_invest` float NOT NULL,
  `daily_income` int(11) NOT NULL DEFAULT 10,
  `money_ini` int(11) NOT NULL DEFAULT 100,
  `return_mitigation` float NOT NULL DEFAULT 0.99,
  `time_span` int(3) NOT NULL DEFAULT 60,
  `p_property` float NOT NULL DEFAULT 0.40606,
  `p_fatality` float NOT NULL DEFAULT 0.77575,
  `p_injury` float NOT NULL DEFAULT 0.36718,
  `dampening_factor_investment` float NOT NULL DEFAULT 0.7,
  `wealth_property` float NOT NULL DEFAULT 0.8,
  `injury_daily_inc_loss` float NOT NULL,
  `fatality_daily_inc_loss` float NOT NULL,
  `age_restriction` int(3) NOT NULL DEFAULT 18,
  `day_initial_temporal` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `param`
--

INSERT INTO `param` (`timestamp`, `scenario_id`, `comments`, `weight_invest`, `daily_income`, `money_ini`, `return_mitigation`, `time_span`, `p_property`, `p_fatality`, `p_injury`, `dampening_factor_investment`, `wealth_property`, `injury_daily_inc_loss`, `fatality_daily_inc_loss`, `age_restriction`, `day_initial_temporal`) VALUES
('2015-07-06 23:08:37', 1, 'w0.7_emotion_nosocial', 0.7, 8760, 5000000, 0.84, 20, 0.3, 0.09, 0.9, 1, 0.5, 0.25, 0.5, 18, 1);

-- --------------------------------------------------------

--
-- Table structure for table `property_images`
--

CREATE TABLE `property_images` (
  `sno` int(11) NOT NULL,
  `scenario_id` int(11) NOT NULL,
  `image_source` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `property_images`
--

INSERT INTO `property_images` (`sno`, `scenario_id`, `image_source`) VALUES
(1, 1, 'property_images/property3.jpg'),
(2, 1, 'property_images/property1.jpg'),
(3, 1, 'property_images/property2.jpg'),
(4, 3, 'property_images/property3.jpg'),
(5, 3, 'property_images/property1.jpg'),
(6, 3, 'property_images/property2.jpg'),
(7, 6, 'property_images/property1.jpg'),
(8, 6, 'property_images/property2.jpg'),
(9, 6, 'property_images/property3.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `reference`
--

CREATE TABLE `reference` (
  `day` int(3) NOT NULL DEFAULT 0,
  `p_temporal` decimal(10,9) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_general_ci;

--
-- Dumping data for table `reference`
--

INSERT INTO `reference` (`day`, `p_temporal`) VALUES
(1, 0.088411000),
(2, 0.062823000),
(3, 0.064422000),
(4, 0.059965000),
(5, 0.218549000),
(6, 0.674991000),
(7, 0.878744000),
(8, 0.332772000),
(9, 0.043983000),
(10, 0.024852000),
(11, 0.032376000),
(12, 0.084888000),
(13, 0.088411000),
(14, 0.062823000),
(15, 0.064422000),
(16, 0.059965000),
(17, 0.218549000),
(18, 0.674991000),
(19, 0.878744000),
(20, 0.332772000),
(21, 0.043983000),
(22, 0.024852000),
(23, 0.032376000),
(24, 0.084888000),
(25, 0.088411000),
(26, 0.062823000),
(27, 0.064422000),
(28, 0.059965000),
(29, 0.218549000),
(30, 0.674991000),
(31, 0.878744000),
(32, 0.332772000),
(33, 0.043983000),
(34, 0.024852000),
(35, 0.032376000),
(36, 0.084888000),
(37, 0.088411000),
(38, 0.062823000),
(39, 0.064422000),
(40, 0.059965000),
(41, 0.218549000),
(42, 0.674991000),
(43, 0.878744000),
(44, 0.332772000),
(45, 0.043983000),
(46, 0.024852000),
(47, 0.032376000),
(48, 0.084888000),
(49, 0.088411000),
(50, 0.062823000),
(51, 0.064422000),
(52, 0.059965000),
(53, 0.218549000),
(54, 0.674991000),
(55, 0.878744000),
(56, 0.332772000),
(57, 0.043983000),
(58, 0.024852000),
(59, 0.032376000),
(60, 0.084888000);

-- --------------------------------------------------------

--
-- Table structure for table `spatial_p`
--

CREATE TABLE `spatial_p` (
  `sno` int(11) NOT NULL,
  `low` decimal(2,2) NOT NULL,
  `value` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

--
-- Dumping data for table `spatial_p`
--

INSERT INTO `spatial_p` (`sno`, `low`, `value`) VALUES
(1, 0.05, 0.3274),
(2, 0.10, 0.3389),
(3, 0.15, 0.3523),
(4, 0.20, 0.3644),
(5, 0.25, 0.3783),
(6, 0.30, 0.3902),
(7, 0.35, 0.4039),
(8, 0.40, 0.4149),
(9, 0.45, 0.434),
(10, 0.50, 0.4487),
(11, 0.55, 0.4683),
(12, 0.60, 0.4907),
(13, 0.65, 0.5141),
(14, 0.70, 0.5408),
(15, 0.75, 0.5585),
(16, 0.80, 0.5877),
(17, 0.85, 0.7959),
(18, 0.90, 0.8967),
(19, 0.95, 0.9532),
(21, 0.00, 0),
(22, 0.99, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `death_images`
--
ALTER TABLE `death_images`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `demographic`
--
ALTER TABLE `demographic`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `game`
--
ALTER TABLE `game`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `injury_images`
--
ALTER TABLE `injury_images`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `message_day`
--
ALTER TABLE `message_day`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `message_probability`
--
ALTER TABLE `message_probability`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `nbr_pay`
--
ALTER TABLE `nbr_pay`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `param`
--
ALTER TABLE `param`
  ADD PRIMARY KEY (`scenario_id`);

--
-- Indexes for table `property_images`
--
ALTER TABLE `property_images`
  ADD PRIMARY KEY (`sno`);

--
-- Indexes for table `spatial_p`
--
ALTER TABLE `spatial_p`
  ADD PRIMARY KEY (`sno`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `death_images`
--
ALTER TABLE `death_images`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `demographic`
--
ALTER TABLE `demographic`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `game`
--
ALTER TABLE `game`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=43;

--
-- AUTO_INCREMENT for table `injury_images`
--
ALTER TABLE `injury_images`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `message_day`
--
ALTER TABLE `message_day`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `message_probability`
--
ALTER TABLE `message_probability`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `nbr_pay`
--
ALTER TABLE `nbr_pay`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `param`
--
ALTER TABLE `param`
  MODIFY `scenario_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `property_images`
--
ALTER TABLE `property_images`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `spatial_p`
--
ALTER TABLE `spatial_p`
  MODIFY `sno` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
