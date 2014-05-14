create table problem (
	name varchar(64) primary key,
	`exists` tinyint not null,
	time datetime not null
);

create table sensor (
	name varchar(64) primary key,
	time datetime not null,
	value text not null
);
