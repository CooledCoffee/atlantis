create table problem (
	name varchar(64) primary key,
	enabled tinyint not null default 1,
	`exists` tinyint not null
);

create table sensor (
	name varchar(64) primary key,
	error_rate float,
	time datetime,
	value text
);

create table solution (
	name varchar(64) primary key,
	applied tinyint not null,
	enabled tinyint not null default 1
);
