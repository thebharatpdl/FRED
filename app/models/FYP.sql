-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Feb 12, 2024 at 06:30 PM
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
-- Database: `FYP`
--

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(200) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `password`) VALUES
(1, 'Biroshan Kumar Mahato', 'biroshan.singh72@gmail.com', '$2b$12$YGmw6WrHeX.eCKhBewDqPuvEG0vez3PXSZ/MljVFkuVX7wD5opT7y'),
(2, 'Sanam Shivakoti', 'saman@gmail.com', '$2b$12$xP7C/uySpygFc4cblljSFeyPtyEw4bFqP.KhcR/rgpwU9.rhNKkiC'),
(3, 'Biroshan Kumar Mahato', 'biroshan.singh71@gmail.com', '$2b$12$bxg//eaBV/JCFpWT1US.r.WaGfe48YptC8Hjh1B/pLBziD9BbFqE2'),
(4, 'Aashish', 'aashish@gmail.com', '$2b$12$5lKC2LK4hefqVK4Cxe8zpua.VZNOKaqOsx/V8KG6zuSjF5q4w8P26'),
(5, 'san', 'san@gmail.com', '$2b$12$aZcFUpI5HdsxQdKfwVxof.FhdOwMNsSFCpGRfBgbqTeWu5f.Pw8Zm');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
