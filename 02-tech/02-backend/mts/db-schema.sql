


create database mts;
use mts;

create table accounts (
    number varchar(20) primary key,
    balance decimal(10,2) not null
);

insert into accounts (number, balance) values
('1234567890', 1000.00),
('0987654321', 500.00);

insert into accounts (number, balance) values
('1111111111', 2000.00),
('2222222222', 1500.00);