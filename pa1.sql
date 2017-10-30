/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : pa1

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-10-30 16:40:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for albums
-- ----------------------------
DROP TABLE IF EXISTS `albums`;
CREATE TABLE `albums` (
  `album_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` char(20) DEFAULT NULL,
  `date_of_creation` datetime DEFAULT NULL,
  `user_id` int(20) NOT NULL,
  PRIMARY KEY (`album_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of albums
-- ----------------------------
INSERT INTO `albums` VALUES ('1', 'hehe', null, '12');
INSERT INTO `albums` VALUES ('13', 'test', '2017-10-16 02:29:52', '12');
INSERT INTO `albums` VALUES ('17', 'haha', '2017-10-28 12:06:58', '14');
INSERT INTO `albums` VALUES ('18', 'new page', '2017-10-29 02:11:55', '12');
INSERT INTO `albums` VALUES ('20', 'ttest', '2017-10-29 13:02:53', '12');
INSERT INTO `albums` VALUES ('21', 'lala', '2017-10-29 21:33:55', '23');

-- ----------------------------
-- Table structure for associate
-- ----------------------------
DROP TABLE IF EXISTS `associate`;
CREATE TABLE `associate` (
  `tag` char(100) NOT NULL,
  `photo_id` int(11) NOT NULL,
  PRIMARY KEY (`tag`,`photo_id`),
  KEY `photo_id` (`photo_id`),
  CONSTRAINT `associate_ibfk_1` FOREIGN KEY (`tag`) REFERENCES `tags` (`tag`) ON DELETE CASCADE,
  CONSTRAINT `associate_ibfk_2` FOREIGN KEY (`photo_id`) REFERENCES `photos` (`photo_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of associate
-- ----------------------------
INSERT INTO `associate` VALUES ('aa', '2');
INSERT INTO `associate` VALUES ('bb', '2');
INSERT INTO `associate` VALUES ('ans', '12');
INSERT INTO `associate` VALUES ('bl', '13');
INSERT INTO `associate` VALUES ('yellow', '16');
INSERT INTO `associate` VALUES ('yy', '16');

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `commtent_id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `date_of_comment` datetime DEFAULT NULL,
  `user_id` char(20) DEFAULT NULL,
  `photo_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`commtent_id`),
  KEY `photo_id` (`photo_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`photo_id`) REFERENCES `photos` (`photo_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------
INSERT INTO `comments` VALUES ('1', 'hahha', '2017-10-28 17:43:10', '', '2');
INSERT INTO `comments` VALUES ('2', '1123', '2017-10-28 17:45:22', '', '2');
INSERT INTO `comments` VALUES ('3', 'ni hao', '2017-10-28 17:56:47', '17', null);
INSERT INTO `comments` VALUES ('4', '123', '2017-10-29 03:53:24', '16', '2');
INSERT INTO `comments` VALUES ('5', 'lalala', '2017-10-29 04:21:04', '16', '12');
INSERT INTO `comments` VALUES ('6', 'haha', '2017-10-29 21:11:09', '', null);
INSERT INTO `comments` VALUES ('7', 'i did not log in', '2017-10-29 21:29:56', '', null);
INSERT INTO `comments` VALUES ('8', 'lalallalalajkfljlasd', '2017-10-30 16:09:55', '', '2');
INSERT INTO `comments` VALUES ('9', 'asdfjlasdjf', '2017-10-30 16:36:53', '', null);

-- ----------------------------
-- Table structure for friends
-- ----------------------------
DROP TABLE IF EXISTS `friends`;
CREATE TABLE `friends` (
  `user_id1` int(20) NOT NULL,
  `user_id2` int(20) NOT NULL,
  PRIMARY KEY (`user_id1`,`user_id2`),
  KEY `user_id2` (`user_id2`),
  CONSTRAINT `user_id1` FOREIGN KEY (`user_id1`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of friends
-- ----------------------------
INSERT INTO `friends` VALUES ('12', '12');
INSERT INTO `friends` VALUES ('13', '12');
INSERT INTO `friends` VALUES ('16', '12');
INSERT INTO `friends` VALUES ('17', '12');
INSERT INTO `friends` VALUES ('12', '13');
INSERT INTO `friends` VALUES ('14', '13');
INSERT INTO `friends` VALUES ('13', '14');
INSERT INTO `friends` VALUES ('15', '14');
INSERT INTO `friends` VALUES ('14', '15');
INSERT INTO `friends` VALUES ('12', '16');
INSERT INTO `friends` VALUES ('16', '16');
INSERT INTO `friends` VALUES ('22', '16');
INSERT INTO `friends` VALUES ('12', '17');
INSERT INTO `friends` VALUES ('16', '22');

-- ----------------------------
-- Table structure for likes
-- ----------------------------
DROP TABLE IF EXISTS `likes`;
CREATE TABLE `likes` (
  `user_id` int(20) NOT NULL,
  `photo_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`photo_id`),
  KEY `photo_id` (`photo_id`),
  CONSTRAINT `likes_ibfk_2` FOREIGN KEY (`photo_id`) REFERENCES `photos` (`photo_id`) ON DELETE CASCADE,
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of likes
-- ----------------------------
INSERT INTO `likes` VALUES ('16', '2');
INSERT INTO `likes` VALUES ('22', '2');
INSERT INTO `likes` VALUES ('16', '12');
INSERT INTO `likes` VALUES ('24', '12');
INSERT INTO `likes` VALUES ('12', '15');

-- ----------------------------
-- Table structure for photos
-- ----------------------------
DROP TABLE IF EXISTS `photos`;
CREATE TABLE `photos` (
  `photo_id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` text,
  `album_id` int(11) DEFAULT NULL,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`photo_id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `album_id` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of photos
-- ----------------------------
INSERT INTO `photos` VALUES ('2', 'rr', '13', '/static/img/2.png');
INSERT INTO `photos` VALUES ('12', '530answer', '1', '/static/img/12.PNG');
INSERT INTO `photos` VALUES ('13', 'new blue', '1', '/static/img/13.png');
INSERT INTO `photos` VALUES ('15', 'aaa', '17', '/static/img/imm.png');
INSERT INTO `photos` VALUES ('16', 'my first photo', '21', '/static/img/16.png');

-- ----------------------------
-- Table structure for tags
-- ----------------------------
DROP TABLE IF EXISTS `tags`;
CREATE TABLE `tags` (
  `tag` char(100) NOT NULL,
  PRIMARY KEY (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of tags
-- ----------------------------
INSERT INTO `tags` VALUES ('12');
INSERT INTO `tags` VALUES ('31');
INSERT INTO `tags` VALUES ('aa');
INSERT INTO `tags` VALUES ('ans');
INSERT INTO `tags` VALUES ('bb');
INSERT INTO `tags` VALUES ('bl');
INSERT INTO `tags` VALUES ('cc');
INSERT INTO `tags` VALUES ('yellow');
INSERT INTO `tags` VALUES ('yy');

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(20) NOT NULL AUTO_INCREMENT,
  `first_name` char(20) DEFAULT NULL,
  `last_name` char(20) DEFAULT NULL,
  `email` char(50) DEFAULT NULL,
  `date_of_birth` datetime DEFAULT NULL,
  `hometown` char(50) DEFAULT NULL,
  `gender` int(11) DEFAULT NULL,
  `password` char(20) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('12', '', '', 'hah@gmail.com', null, '', '1', '12');
INSERT INTO `users` VALUES ('13', '', '', 'ya@gmail.com', '1994-11-19 00:00:00', '', '1', '12');
INSERT INTO `users` VALUES ('14', null, null, 'lala@gmail.com', null, null, null, 'qwe');
INSERT INTO `users` VALUES ('15', null, null, 'mess@gmail.com', null, null, null, '123');
INSERT INTO `users` VALUES ('16', null, null, 'tt@gmail.com', null, null, null, '444');
INSERT INTO `users` VALUES ('17', 'wo', 'ni', 'tz@gmail.com', '2017-10-15 00:00:00', 'suzhou', '1', 'www');
INSERT INTO `users` VALUES ('18', 't', 'z', 'zt@163.com', '2017-10-13 00:00:00', 'ss', '1', 'qqq');
INSERT INTO `users` VALUES ('19', 'z', 't', 'tuzhong1994@gmail.com', '2017-10-25 00:00:00', 'as', '1', '222');
INSERT INTO `users` VALUES ('20', '', '', 'aa@gmail.com', '2017-10-12 00:00:00', '', '1', '123');
INSERT INTO `users` VALUES ('21', '', '', '', '2017-10-13 00:00:00', '123', '1', '14');
INSERT INTO `users` VALUES ('22', '', '', '111@gmail.com', '2017-10-05 00:00:00', 'h123', '1', 'hhhh');
INSERT INTO `users` VALUES ('23', 'zhong', 'tu', 'tuz@gmail.com', '2017-10-14 00:00:00', 'suzhou', '1', 'qwe');
INSERT INTO `users` VALUES ('24', '', '', 'ty@gmail.com', '2017-10-28 00:00:00', '123213', '1', '123');
