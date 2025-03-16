-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 16, 2025 at 06:31 PM
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
-- Database: `ql_truyen`
--
CREATE DATABASE IF NOT EXISTS `ql_truyen` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `ql_truyen`;

-- --------------------------------------------------------

--
-- Table structure for table `tbchitietdonban`
--

CREATE TABLE `tbchitietdonban` (
  `machitiet` int(11) NOT NULL,
  `madonban` int(11) DEFAULT NULL,
  `matruyen` int(11) DEFAULT NULL,
  `soluong` int(11) DEFAULT NULL,
  `dongia` decimal(10,2) DEFAULT NULL,
  `thanhtien` decimal(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbchitietdonban`
--

INSERT INTO `tbchitietdonban` (`machitiet`, `madonban`, `matruyen`, `soluong`, `dongia`, `thanhtien`) VALUES
(32, 2, 22, 3, 234.00, 702.00),
(53, 29, 1, 5, 323232.00, 1616160.00),
(123, 122, 22, 4, 22311.00, 89244.00);

-- --------------------------------------------------------

--
-- Table structure for table `tbchitietdonthue`
--

CREATE TABLE `tbchitietdonthue` (
  `machitiet` int(11) NOT NULL,
  `madonthue` int(11) DEFAULT NULL,
  `matruyen` int(11) DEFAULT NULL,
  `soluong` int(11) DEFAULT NULL,
  `ngaythue` date DEFAULT curdate(),
  `ngaytra` date DEFAULT NULL,
  `tinhtrang` enum('Chưa trả','Đã trả') DEFAULT 'Chưa trả'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbchitietdonthue`
--

INSERT INTO `tbchitietdonthue` (`machitiet`, `madonthue`, `matruyen`, `soluong`, `ngaythue`, `ngaytra`, `tinhtrang`) VALUES
(3, 113, 22, 1, '2000-01-01', '2000-01-01', 'Đã trả'),
(13, 14, 22, 12, '2000-01-01', '2000-01-01', 'Đã trả'),
(32, 32, 22, 3, '2000-01-01', '2000-01-01', 'Đã trả'),
(34, 34, 22, 1, '2033-01-01', '2034-01-01', 'Đã trả'),
(44, 44, 22, 3, '2034-01-01', '2035-01-01', 'Đã trả');

-- --------------------------------------------------------

--
-- Table structure for table `tbdonban`
--

CREATE TABLE `tbdonban` (
  `madonban` int(11) NOT NULL,
  `makhach` int(11) DEFAULT NULL,
  `ngayban` date DEFAULT curdate(),
  `tongtien` decimal(10,2) DEFAULT NULL,
  `tinhtrang` enum('Đã thanh toán','Chưa thanh toán') NOT NULL DEFAULT 'Chưa thanh toán'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbdonban`
--

INSERT INTO `tbdonban` (`madonban`, `makhach`, `ngayban`, `tongtien`, `tinhtrang`) VALUES
(2, 2, '3900-01-01', NULL, 'Đã thanh toán'),
(29, 2, '2000-01-01', NULL, 'Đã thanh toán'),
(122, 2, '2032-01-01', NULL, 'Đã thanh toán');

-- --------------------------------------------------------

--
-- Table structure for table `tbdonthue`
--

CREATE TABLE `tbdonthue` (
  `madonthue` int(11) NOT NULL,
  `makhach` int(11) DEFAULT NULL,
  `ngaythue` date DEFAULT curdate(),
  `ngaytra` date DEFAULT NULL,
  `tongtien` decimal(10,2) DEFAULT NULL,
  `tinhtrang` enum('Đang thuê','Đã trả') DEFAULT 'Đang thuê'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbdonthue`
--

INSERT INTO `tbdonthue` (`madonthue`, `makhach`, `ngaythue`, `ngaytra`, `tongtien`, `tinhtrang`) VALUES
(14, 1, '2000-01-01', '2000-01-01', 345678.00, 'Đã trả'),
(32, 2, '2000-01-01', '2000-01-01', 3434.00, 'Đã trả'),
(34, 1, '2033-01-01', '2034-01-01', 132.00, 'Đã trả'),
(44, 2, '2034-01-01', '2035-01-01', 123322.00, 'Đã trả'),
(113, 1, '2032-01-01', '2054-01-01', 345.00, 'Đã trả'),
(122, 1, '2000-01-01', '2000-01-01', 99999999.99, 'Đang thuê'),
(4543, 2, '2000-01-01', '2000-01-01', 12345.00, 'Đang thuê');

-- --------------------------------------------------------

--
-- Table structure for table `tbkhachhang`
--

CREATE TABLE `tbkhachhang` (
  `makhach` int(11) NOT NULL,
  `tenkhach` varchar(255) NOT NULL,
  `tuoi` int(11) DEFAULT NULL,
  `gioitinh` enum('Nam','Nữ','Khác') DEFAULT NULL,
  `sodienthoai` varchar(15) DEFAULT NULL,
  `diachi` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbkhachhang`
--

INSERT INTO `tbkhachhang` (`makhach`, `tenkhach`, `tuoi`, `gioitinh`, `sodienthoai`, `diachi`) VALUES
(1, 'Hưng', 1, 'Nữ', '123', 'Đống Đa'),
(2, 'lam', 22, 'Nữ', '123456789', 'hn');

-- --------------------------------------------------------

--
-- Table structure for table `tbtaikhoan`
--

CREATE TABLE `tbtaikhoan` (
  `id` int(11) NOT NULL,
  `tennguoidung` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `matkhau` varchar(255) NOT NULL,
  `sodienthoai` varchar(15) DEFAULT NULL,
  `token_reset` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbtaikhoan`
--

INSERT INTO `tbtaikhoan` (`id`, `tennguoidung`, `email`, `matkhau`, `sodienthoai`, `token_reset`) VALUES
(1, 'hung', 'hung@gmail.com', '321', '12345667', NULL),
(2, 'lam', 'lam@gmail.com', '345', '0986329841', NULL),
(3, 'Vuongtuanhung', '123@gmail.com', '123', '123456789', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `tbtruyen`
--

CREATE TABLE `tbtruyen` (
  `matruyen` int(11) NOT NULL,
  `tentruyen` varchar(255) NOT NULL,
  `theloai` varchar(100) DEFAULT NULL,
  `tacgia` varchar(255) DEFAULT NULL,
  `soluong` int(11) DEFAULT NULL,
  `dongia` decimal(10,2) DEFAULT NULL,
  `giathue` decimal(10,2) DEFAULT NULL,
  `ngayphathanh` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tbtruyen`
--

INSERT INTO `tbtruyen` (`matruyen`, `tentruyen`, `theloai`, `tacgia`, `soluong`, `dongia`, `giathue`, `ngayphathanh`) VALUES
(1, 'tht', 'fgerg', 'ửgrg', 1234, 234543.00, 1232.00, '1999-12-12'),
(22, 'jack bo con', 'tamly', 'dfrg', 1234, 123456.00, 2345.00, '2000-01-01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbchitietdonban`
--
ALTER TABLE `tbchitietdonban`
  ADD PRIMARY KEY (`machitiet`),
  ADD KEY `madonban` (`madonban`),
  ADD KEY `matruyen` (`matruyen`);

--
-- Indexes for table `tbchitietdonthue`
--
ALTER TABLE `tbchitietdonthue`
  ADD PRIMARY KEY (`machitiet`),
  ADD KEY `madonthue` (`madonthue`),
  ADD KEY `matruyen` (`matruyen`);

--
-- Indexes for table `tbdonban`
--
ALTER TABLE `tbdonban`
  ADD PRIMARY KEY (`madonban`),
  ADD KEY `makhach` (`makhach`);

--
-- Indexes for table `tbdonthue`
--
ALTER TABLE `tbdonthue`
  ADD PRIMARY KEY (`madonthue`),
  ADD KEY `makhach` (`makhach`);

--
-- Indexes for table `tbkhachhang`
--
ALTER TABLE `tbkhachhang`
  ADD PRIMARY KEY (`makhach`);

--
-- Indexes for table `tbtaikhoan`
--
ALTER TABLE `tbtaikhoan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `tennguoidung` (`tennguoidung`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `tbtruyen`
--
ALTER TABLE `tbtruyen`
  ADD PRIMARY KEY (`matruyen`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbchitietdonban`
--
ALTER TABLE `tbchitietdonban`
  MODIFY `machitiet` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1232;

--
-- AUTO_INCREMENT for table `tbchitietdonthue`
--
ALTER TABLE `tbchitietdonthue`
  MODIFY `machitiet` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=45;

--
-- AUTO_INCREMENT for table `tbdonban`
--
ALTER TABLE `tbdonban`
  MODIFY `madonban` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=325;

--
-- AUTO_INCREMENT for table `tbdonthue`
--
ALTER TABLE `tbdonthue`
  MODIFY `madonthue` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4544;

--
-- AUTO_INCREMENT for table `tbkhachhang`
--
ALTER TABLE `tbkhachhang`
  MODIFY `makhach` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tbtaikhoan`
--
ALTER TABLE `tbtaikhoan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tbtruyen`
--
ALTER TABLE `tbtruyen`
  MODIFY `matruyen` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tbchitietdonban`
--
ALTER TABLE `tbchitietdonban`
  ADD CONSTRAINT `tbchitietdonban_ibfk_1` FOREIGN KEY (`madonban`) REFERENCES `tbdonban` (`madonban`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbchitietdonban_ibfk_2` FOREIGN KEY (`matruyen`) REFERENCES `tbtruyen` (`matruyen`) ON DELETE CASCADE;

--
-- Constraints for table `tbchitietdonthue`
--
ALTER TABLE `tbchitietdonthue`
  ADD CONSTRAINT `tbchitietdonthue_ibfk_1` FOREIGN KEY (`madonthue`) REFERENCES `tbdonthue` (`madonthue`) ON DELETE CASCADE,
  ADD CONSTRAINT `tbchitietdonthue_ibfk_2` FOREIGN KEY (`matruyen`) REFERENCES `tbtruyen` (`matruyen`) ON DELETE CASCADE;

--
-- Constraints for table `tbdonban`
--
ALTER TABLE `tbdonban`
  ADD CONSTRAINT `tbdonban_ibfk_1` FOREIGN KEY (`makhach`) REFERENCES `tbkhachhang` (`makhach`) ON DELETE CASCADE;

--
-- Constraints for table `tbdonthue`
--
ALTER TABLE `tbdonthue`
  ADD CONSTRAINT `tbdonthue_ibfk_1` FOREIGN KEY (`makhach`) REFERENCES `tbkhachhang` (`makhach`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
