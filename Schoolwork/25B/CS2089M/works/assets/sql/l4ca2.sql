USE Banking;

DROP USER IF EXISTS 'user001'@'%';
CREATE USER 'user001'@'%' IDENTIFIED BY '123456';

SELECT user, host FROM mysql.user WHERE user = 'user001';

GRANT SELECT, INSERT ON Banking.employee TO 'user001'@'%';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'user001'@'%';

REVOKE INSERT ON Banking.employee FROM 'user001'@'%';

SHOW GRANTS FOR 'user001'@'%';
