drop table if exists MSGS;
drop table if exists USERS;

CREATE TABLE `MSGS` (
	`UserId`	TEXT UNIQUE,
	`Message`	TEXT,
	`TimeStamp`	INTEGER,
	`GroupId`	INTEGER,
	`GroupName`	TEXT,
	`RecipientList`	TEXT,
	PRIMARY KEY(`UserId`)
);

CREATE TABLE `USERS` (
	`UserId`	TEXT UNIQUE,
	`UserNameF`	TEXT,
	`UserNameL`	TEXT,
	`PasswordHash`	TEXT,
	`GroupId`	INTEGER,
	PRIMARY KEY(`UserId`)
);