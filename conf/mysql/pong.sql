CREATE DATABASE IF NOT EXISTS pong;

CREATE USER IF NOT EXISTS 'pong' IDENTIFIED BY 'pongpong';
GRANT ALL PRIVILEGES ON pong.* TO 'pong';

USE pong;

CREATE TABLE IF NOT EXISTS `users_auth` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`name` varchar(255) NOT NULL,
`password` varchar(255) NOT NULL,
PRIMARY KEY (`id`),
UNIQUE KEY `name_idx` (`name`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `leaderboard` (
`id` int(11) NOT NULL AUTO_INCREMENT,
`user` varchar(255) NOT NULL,
`wins` int(11) DEFAULT NULL,
`losses` int(11) DEFAULT NULL,
`winrate` float DEFAULT NULL,
PRIMARY KEY (`id`),
KEY `winrate_idx` (`winrate` DESC) USING BTREE
) ENGINE=InnoDB;
