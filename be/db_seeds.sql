USE simstore;

INSERT INTO `role` 
	(id, role_name)
VALUES 
	(1,'admin'),
	(2,'employee');

SELECT * FROM `role`;

INSERT INTO `employee` 
	(id, full_name, date_of_birth, gender, citizen_id, phone_number, email, address, avatar, status)
VALUES 
	(1,'Nguyễn Sơn','1990-10-30',1,'098743565456','0978907867','sonnguyen@gmail.com','97 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',1),
	(2,'Trần Thị Anh','1991-08-26',0,'087956789045','0965478965','anhtran@gmail.com','98 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',1),
	(3,'Nguyễn Hoàng Tiến','1994-07-23',1,'077890564756','0998567435','tiennguyen@gmail.com','90 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',1),
	(4,'Trần Thị Dung','1995-05-24',0,'067876756789','0932456789','dungtran@gmail.com','91 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',0),
	(5,'Nguyễn Thị Vân','1996-09-18',0,'056789678978','0943786789','vannguyen@gmail.com','96 man thiện, Hiệp Phú, Tp. Thủ Đức, Tp. HCM','',1);

SELECT * FROM `employee`;

INSERT INTO `account` 
	(id, username, password, role_id, employee_id, is_active)
VALUES 
	(1,'admin1','admin1',1,1,1),
	(2,'admin2','admin2',1,2,1),
	(3,'employee1','employee1',2,3,1),
	(4,'emplyee2','employee2',2,4,1),
	(5,'employee3','employee3',2,5,1);
    
SELECT * FROM `account`;



INSERT INTO `supplier` 
	(id, name, phone_number, email, address, status)
VALUES 
	(1,'Vinaphone Center','0486235791','supportbussiness@vinaphone.com','số 57 Huỳnh Thúc Kháng, P. Láng Hạ, Q. Đống Đa, TP. Hà Nội',1),
	(2,'Mobifone Center','0197648536','supportbussiness@mobifone.com','182-184, Đường Lê Lợi, Khóm. Châu Quới,  P. Châu Phú B, Tp. Châu Đốc, tỉnh An Giang',0),
	(3,'Viettel Center','0123586497','supportbussiness@viettel.com','Lô D26, Khu đô thị mới Cầu Giấy, phường Yên Hòa, quận Cầu Giấy, Hà Nội',1),
	(4,'Vietnammobile Company','06452452635','bussinesscenter@vnmobile.com','98 Tôn Thất Tùng, Phường Bến Thành, Quận 1, TP. Hồ Chí Minh',1),
	(5,'Gmobile Company','04831956894','bussinesscenter@gmobile.com','280B Lạc Long Quân, Quận Tây Hồ, Thành phố Hà Nội',0);

SELECT * FROM `supplier`;

INSERT INTO `importreceipt` 
	(id, created_at, note, supplier_id, employee_id)
VALUES 
	(1,'2025-01-12 16:44:00','Đợt nhập các sim thông thường',1,2),
	(2,'2025-01-16 14:58:00','',3,4),
	(3,'2025-01-22 10:05:00','Đợt nhập các sim số đẹp',1,3);

SELECT * FROM `importreceipt`;



INSERT INTO `category1` 
	(id, name, description)
VALUES 
	(1,'Cam Kết',''),
	(2,'Trả Trước',''),
	(3,'Trả Sau','');

SELECT * FROM `category1`;

INSERT INTO `category2` 
	(id, name, description)
VALUES 
	(1,'Số đẹp',''),
	(2,'Siêu vip',''),
	(3,'Lục Quý',''),
	(4,'Ngũ Quý',''),
	(5,'Tứ Quý',''),
	(6,'Tam Hoa',''),
	(7,'Số Kép','');

SELECT * FROM `category2`;

INSERT INTO `mobilenetworkoperator` 
	(id, name)
VALUES 
	(1,'Vinaphone'),
	(2,'Mobifone'),
	(3,'Viettel'),
	(4,'Vietnammobile'),
	(5,'Gmobile');

SELECT * FROM `mobilenetworkoperator`;

INSERT INTO `sim` 
	(id, phone_number, mobile_network_operator_id, category_1_id, category_2_id, employee_id, export_price, status, created_at)
VALUES 
	(1,'0987654321',3,1,4,1,5000000.00,1,'2025-02-12 10:00:00'),
	(2,'0971234567',3,2,6,2,2000000.00,2,'2025-02-13 03:14:00'),
	(3,'0912345678',1,3,1,3,8000000.00,0,'2025-02-14 03:14:00'),
	(4,'0908765432',2,2,5,4,3000000.00,1,'2025-02-15 03:14:00'),
	(5,'0931122334',2,1,2,5,1500000.00,2,'2025-02-16 03:14:00'),
	(6,'0321456789',4,3,7,1,1200000.00,1,'2025-02-17 03:14:00'),
	(7,'0869998888',5,1,6,2,9500000.00,0,'2025-02-18 03:14:00'),
	(8,'0886665555',3,2,4,3,4000000.00,2,'2025-02-19 03:14:00'),
	(9,'0897774444',3,3,5,4,6000000.00,1,'2025-02-20 03:14:00'),
	(10,'0963332222',1,1,3,1,7000000.00,0,'2025-02-21 03:14:00'),
	(11,'0945551111',1,2,6,2,2200000.00,1,'2025-02-22 03:14:00'),
	(12,'0924447777',2,3,7,3,3500000.00,2,'2025-02-23 03:14:00'),
	(13,'0341119999',4,1,2,4,5000000.00,1,'2025-02-24 03:14:00'),
	(14,'0352228888',4,2,3,2,4200000.00,0,'2025-02-25 03:14:00'),
	(15,'0363337777',4,3,1,1,7500000.00,2,'2025-02-26 03:14:00'),
	(16,'0374446666',5,1,4,4,1300000.00,1,'2025-02-27 03:14:00'),
	(17,'0385555555',5,2,6,3,2700000.00,0,'2025-02-28 03:14:00'),
	(18,'0396664444',5,3,7,4,3000000.00,2,'2025-03-01 03:14:00'),
	(19,'0707773333',2,1,2,5,5000000.00,1,'2025-03-02 03:14:00'),
	(20,'0778882222',3,2,5,5,6500000.00,0,'2025-03-03 03:14:00');

SELECT * FROM `sim`;

INSERT INTO `province` 
	(id, name)
VALUES 
	(1,'An Giang'),
	(2,'Bà Rịa - Vũng Tàu'),
	(3,'Bạc Liêu'),
	(4,'Bắc Giang'),
	(5,'Bắc Kạn'),
	(6,'Bắc Ninh'),
	(7,'Bến Tre'),
	(8,'Bình Định'),
	(9,'Bình Dương'),
	(10,'Bình Phước'),
	(11,'Bình Thuận'),
	(12,'Cà Mau'),
	(13,'Cần Thơ'),
	(14,'Cao Bằng'),
	(15,'Đà Nẵng'),
	(16,'Đắk Lắk'),
	(17,'Đắk Nông'),
	(18,'Điện Biên'),
	(19,'Đồng Nai'),
	(20,'Đồng Tháp'),
	(21,'Gia Lai'),
	(22,'Hà Giang'),
	(23,'Hà Nam'),
	(24,'Hà Nội'),
	(25,'Hà Tĩnh'),
	(26,'Hải Dương'),
	(27,'Hải Phòng'),
	(28,'Hậu Giang'),
	(29,'Hòa Bình'),
	(30,'Hồ Chí Minh'),
	(31,'Hưng Yên'),
	(32,'Khánh Hòa'),
	(33,'Kiên Giang'),
	(34,'Kon Tum'),
	(35,'Lai Châu'),
	(36,'Lâm Đồng'),
	(37,'Lạng Sơn'),
	(38,'Lào Cai'),
	(39,'Long An'),
	(40,'Nam Định'),
	(41,'Nghệ An'),
	(42,'Ninh Bình'),
	(43,'Ninh Thuận'),
	(44,'Phú Thọ'),
	(45,'Phú Yên'),
	(46,'Quảng Bình'),
	(47,'Quảng Nam'),
	(48,'Quảng Ngãi'),
	(49,'Quảng Ninh'),
	(50,'Quảng Trị'),
	(51,'Sóc Trăng'),
	(52,'Sơn La'),
	(53,'Tây Ninh'),
	(54,'Thái Bình'),
	(55,'Thái Nguyên'),
	(56,'Thanh Hóa'),
	(57,'Thừa Thiên Huế'),
	(58,'Tiền Giang'),
	(59,'Trà Vinh'),
	(60,'Tuyên Quang'),
	(61,'Vĩnh Long'),
	(62,'Vĩnh Phúc'),
	(63,'Yên Bái');

SELECT * FROM `province`;

INSERT INTO `district` 
	(id, name, province_id)
VALUES 
	(1,'Quận 1',30),
	(2,'Quận 3',30),
	(3,'Quận 5',30),
	(4,'Quận 7',30),
	(5,'Quận Bình Thạnh',30),
	(6,'Quận Gò Vấp',30),
	(7,'Huyện Bình Chánh',30),
	(8,'Huyện Củ Chi',30),
	(9,'Quận Ba Đình',24),
	(10,'Quận Hoàn Kiếm',24),
	(11,'Quận Hai Bà Trưng',24),
	(12,'Quận Đống Đa',24),
	(13,'Quận Cầu Giấy',24),
	(14,'Quận Thanh Xuân',24),
	(15,'Quận Long Biên',24),
	(16,'Quận Nam Từ Liêm',24),
	(17,'Quận Bắc Từ Liêm',24),
	(18,'Quận Hà Đông',24),
	(19,'Huyện Gia Lâm',24),
	(20,'Huyện Đông Anh',24),
	(21,'Huyện Sóc Sơn',24),
	(22,'Huyện Thanh Trì',24),
	(23,'Quận Hải Châu',15),
	(24,'Quận Thanh Khê',15),
	(25,'Quận Sơn Trà',15),
	(26,'Quận Ngũ Hành Sơn',15),
	(27,'Quận Liên Chiểu',15),
	(28,'Huyện Hòa Vang',15),
	(29,'Thành phố Biên Hòa',19),
	(30,'Thành phố Long Khánh',19),
	(31,'Huyện Nhơn Trạch',19),
	(32,'Huyện Trảng Bom',19),
	(33,'Huyện Long Thành',19),
	(34,'Huyện Vĩnh Cửu',19),
	(35,'Thành phố Thủ Dầu Một',17),
	(36,'Thành phố Thuận An',17),
	(37,'Thành phố Dĩ An',17),
	(38,'Huyện Bến Cát',17),
	(39,'Huyện Tân Uyên',17),
	(40,'Thành phố Nha Trang',21),
	(41,'Thành phố Cam Ranh',21),
	(42,'Huyện Vạn Ninh',21),
	(43,'Huyện Diên Khánh',21),
	(44,'Huyện Cam Lâm',21),
	(45,'Huyện Khánh Vĩnh',21),
	(46,'Thành phố Huế',26),
	(47,'Huyện Phú Vang',26),
	(48,'Huyện Hương Trà',26),
	(49,'Huyện Hương Thủy',26),
	(50,'Thành phố Đà Lạt',14),
	(51,'Thành phố Bảo Lộc',14),
	(52,'Huyện Di Linh',14),
	(53,'Huyện Lạc Dương',14),
	(54,'Huyện Đức Trọng',14),
	(55,'Thành phố Vũng Tàu',18),
	(56,'Thành phố Bà Rịa',18),
	(57,'Huyện Long Điền',18),
	(58,'Huyện Đất Đỏ',18),
	(59,'Huyện Xuyên Mộc',18),
	(60,'Thành phố Cần Thơ',31),
	(61,'Quận Ninh Kiều',31),
	(62,'Quận Bình Thủy',31),
	(63,'Huyện Cờ Đỏ',31),
	(64,'Huyện Thới Lai',31);

SELECT * FROM `district`;

INSERT INTO `ward` 
	(id, name, district_id)
VALUES 
	(1,'Phường Bến Nghé',1),
	(2,'Phường Bến Thành',1),
	(3,'Phường Nguyễn Thái Bình',1),
	(4,'Phường Cô Giang',1),
	(5,'Phường Võ Thị Sáu',2),
	(6,'Phường 7',2),
	(7,'Phường 8',2),
	(8,'Phường 9',2),
	(9,'Phường 10',2),
	(10,'Phường 11',2),
	(11,'Phường 12',2),
	(12,'Phường 13',2),
	(13,'Phường 1',3),
	(14,'Phường 2',3),
	(15,'Phường 3',3),
	(16,'Phường 4',3),
	(17,'Phường 5',3),
	(18,'Phường 6',3),
	(19,'Phường 7',3),
	(20,'Phường 8',3),
	(21,'Phường 9',3),
	(22,'Phường 10',3),
	(23,'Phường 11',3),
	(24,'Phường 12',3),
	(25,'Phường An Hải Bắc',25),
	(26,'Phường An Hải Tây',25),
	(27,'Phường Nại Hiên Đông',25),
	(28,'Phường Thọ Quang',25),
	(29,'Phường Hòa Cường Bắc',23),
	(30,'Phường Hòa Cường Nam',23),
	(31,'Phường Bình Thuận',23),
	(32,'Phường Hải Châu I',23),
	(33,'Phường Hải Châu II',23),
	(34,'Phường Thanh Bình',23),
	(35,'Phường Vĩnh Trung',24),
	(36,'Phường Tân Chính',24),
	(37,'Phường Chính Gián',24),
	(38,'Phường Thạc Gián',24),
	(39,'Phường An Khê',24),
	(40,'Phường Hòa Khê',24),
	(41,'Phường Hòa Hiệp Nam',27),
	(42,'Phường Hòa Hiệp Bắc',27),
	(43,'Phường Hòa Khánh Bắc',27),
	(44,'Phường Hòa Khánh Nam',27),
	(45,'Phường Hòa Minh',27),
	(46,'Phường An Hòa',61),
	(47,'Phường An Nghiệp',61),
	(48,'Phường Cái Khế',61),
	(49,'Phường Xuân Khánh',61),
	(50,'Phường Thới Bình',61),
	(51,'Phường Trà An',62),
	(52,'Phường Trà Nóc',62),
	(53,'Phường Thới Hòa',62),
	(54,'Phường Hưng Phú',62);

SELECT * FROM `ward`;