create table problem (
	name varchar(64) primary key,
	`exists` tinyint not null
);

create table sensor (
	name varchar(64) primary key,
	time datetime not null,
	value text not null
);

create table solution (
	name varchar(64) primary key,
	applied tinyint not null,
	data text
);
