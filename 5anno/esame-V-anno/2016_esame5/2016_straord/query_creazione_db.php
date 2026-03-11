create database iotmedici
 
create table if not exists asl
( id int(8) auto_increment primary key,  
  nome varchar(50) not null,
  indirizzo varchar(50),  
  email varchar(30),  
  telefono varchar(30));
 
create table if not exists medici 
( id int(8) auto_increment primary key,
  codicefiscale char(16) not null,
  nomecognome varchar(50) not null,
  username varchar(30),
  password varchar(32),
  indirizzo varchar(50),  
  email varchar(30), 
  telefono varchar(30)); 
 

create table if not exists dispositivi 
( id int(8) auto_increment primary key,  
  nome varchar(50) not null,
  codice varchar(30) not null,
  informazioni text);

create table if not exists misurazioni
( id int(8) auto_increment primary key,  
  data_ora datetime,
  parametro  varchar(30),
  um varchar(10), 
  valorerilevato decimal(8,2),
  idpaziente int(8),
  codicedispositivo varchar(30),
  foreign key (idpaziente)  references pazienti(id),
  foreign key (codicedispositivo)  references dispositivi(codice));

create table if not exists pazienti
( id int(8) auto_increment primary key,
  codicefiscale char (16) not null,
  nomecognome varchar(50) not null,
  sesso char (1),
  dnascita date,
  indirizzo varchar(50),  
  email varchar(30), 
  telefono varchar(30),
  idasl int(8),
  idmedico int(8),
  foreign key (idasl)  references adsl(id),
  foreign key(idmedico) references medici(id) );
