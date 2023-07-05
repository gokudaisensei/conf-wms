CREATE DATABASE IF NOT EXISTS confwms;
CREATE DATABASE IF NOT EXISTS test;
CREATE USER 'superuser' @'%' IDENTIFIED BY 'confwms';
GRANT ALL PRIVILEGES ON confwms.* TO 'superuser' @'%';
GRANT ALL PRIVILEGES ON test.* TO 'superuser' @'%';