USE Banking;

CREATE VIEW hangzhou_employee AS
    SELECT person_name, street
    FROM employee
    WHERE city = 'Hangzhou';

SELECT * FROM hangzhou_employee;

DROP USER IF EXISTS 'user002'@'%';
CREATE USER 'user002'@'%' IDENTIFIED BY '123456';

GRANT SELECT ON Banking.hangzhou_employee TO 'user002'@'%';
FLUSH PRIVILEGES;

SHOW GRANTS FOR 'user002'@'%';
