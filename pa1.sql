/*
Navicat MySQL Data Transfer

Source Server         : localhost_3306
Source Server Version : 50719
Source Host           : 127.0.0.1:3306
Source Database       : pa1

Target Server Type    : MYSQL
Target Server Version : 50719
File Encoding         : 65001

Date: 2017-10-28 13:04:27
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
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of albums
-- ----------------------------
INSERT INTO `albums` VALUES ('1', 'hehe', null, '12');
INSERT INTO `albums` VALUES ('4', 'hehe', '2017-10-02 00:00:00', '12');
INSERT INTO `albums` VALUES ('13', 'test', '2017-10-16 02:29:52', '12');
INSERT INTO `albums` VALUES ('17', 'haha', '2017-10-28 12:06:58', '14');

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
INSERT INTO `associate` VALUES ('cc', '3');
INSERT INTO `associate` VALUES ('aa', '8');
INSERT INTO `associate` VALUES ('bb', '8');
INSERT INTO `associate` VALUES ('cc', '8');

-- ----------------------------
-- Table structure for comments
-- ----------------------------
DROP TABLE IF EXISTS `comments`;
CREATE TABLE `comments` (
  `commtent_id` int(11) NOT NULL AUTO_INCREMENT,
  `content` text,
  `date_of_comment` datetime DEFAULT NULL,
  `user_id` char(20) DEFAULT NULL,
  `photo_id` int(11) NOT NULL,
  PRIMARY KEY (`commtent_id`),
  KEY `photo_id` (`photo_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`photo_id`) REFERENCES `photos` (`photo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of comments
-- ----------------------------

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
INSERT INTO `friends` VALUES ('13', '12');
INSERT INTO `friends` VALUES ('12', '13');

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

-- ----------------------------
-- Table structure for photos
-- ----------------------------
DROP TABLE IF EXISTS `photos`;
CREATE TABLE `photos` (
  `photo_id` int(11) NOT NULL AUTO_INCREMENT,
  `caption` text,
  `album_id` int(11) NOT NULL,
  `data` longblob,
  `path` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`photo_id`),
  KEY `album_id` (`album_id`),
  CONSTRAINT `photos_ibfk_1` FOREIGN KEY (`album_id`) REFERENCES `albums` (`album_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of photos
-- ----------------------------
INSERT INTO `photos` VALUES ('2', 'rr', '13', null, '/static/img/2.png');
INSERT INTO `photos` VALUES ('3', 'bb', '13', null, '/static/img/3.png');
INSERT INTO `photos` VALUES ('8', 'bblue', '1', null, '/static/img/8.png');

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
INSERT INTO `tags` VALUES ('aa');
INSERT INTO `tags` VALUES ('bb');
INSERT INTO `tags` VALUES ('cc');

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
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES ('12', '', '', 'hah@gmail.com', null, '', '1', '12');
INSERT INTO `users` VALUES ('13', '', '', 'ya@gmail.com', '1994-11-19 00:00:00', '', '1', '12');
INSERT INTO `users` VALUES ('14', null, null, 'lala@gmail.com', null, null, null, 'qwe');
INSERT INTO `users` VALUES ('15', null, null, 'mess@gmail.com', null, null, null, '123');
INSERT INTO `users` VALUES ('16', null, null, 'tt@gmail.com', null, null, null, '444');
