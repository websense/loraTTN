create table applications (
	app_key integer NOT NULL PRIMARY KEY autoincrement,
	app_id varchar(255) NOT NULL
);

create table devices (
	dev_key integer NOT NULL PRIMARY KEY autoincrement,
	dev_id varchar(255) NOT NULL,
	hardware_serial varchar(255) NOT NULL
);

create table payload (
	message_id integer NOT NULL PRIMARY KEY,
        raw_payload varchar(255)
);

create table payload_gps_data (
	message_id integer NOT NULL PRIMARY KEY,
	alt NUMERIC(3,1),
	hdop decimal(8,5),
	latitude  decimal(8,5),
	longitude decimal(8,5)
);

create table payload_temp_moisture (
	message_id integer NOT NULL PRIMARY KEY,
	moisture NUMERIC(3,1),
        port integer,
        temperature NUMERIC(3,1)
);

create table payload_unknown_app(
	message_id integer NOT NULL PRIMARY KEY,
	json_text varchar(255)
);

create table metadata (
	message_id integer NOT NULL PRIMARY KEY,
	time DATETIME NOT NULL,
        frequency NUMERIC(3,1),
        modulation VARCHAR(10),
        data_rate VARCHAR(10),
        airtime long integer,
        coding_rate VARCHAR(10)
);


create table message (
	message_id integer NOT NULL PRIMARY KEY autoincrement,
	app_id integer NOT NULL,
	dev_id integer NOT NULL,
	port	 integer NOT NULL,
	counter integer NOT NULL
);

CREATE TABLE gateway (
	gtw_key integer NOT NULL PRIMARY KEY autoincrement,
	gtw_id varchar(255) NOT NULL
);

CREATE TABLE gatewayinfo (
   gtw_info_id integer NOT NULL PRIMARY KEY autoincrement
  ,gtw_key   integer NOT NULL
  ,message_id integer NOT NULL
  ,time_stamp long INTEGER  NOT NULL
  ,time      DATETIME  NOT NULL
  ,channel   INTEGER  NOT NULL
  ,rssi      NUMERIC(3,1) NOT NULL
  ,snr       NUMERIC(3,1) NOT NULL
  ,rf_chain  INTEGER  NOT NULL
  ,latitude  NUMERIC(8,5) NOT NULL
  ,longitude NUMERIC(8,5) NOT NULL
  ,altitude  NUMERIC(3,1)  NOT NULL
);
 		
