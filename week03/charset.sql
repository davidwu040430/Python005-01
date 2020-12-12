show variables like '%character%';
set character_set_server='utf8mb4';

CREATE DATABASE testdb;

CREATE USER 'testuser' IDENTIFIED BY 'testpass8T#';
GRANT ALL ON testdb.* TO 'testuser'@'%';


