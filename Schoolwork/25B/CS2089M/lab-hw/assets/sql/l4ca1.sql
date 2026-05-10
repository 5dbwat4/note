DROP DATABASE IF EXISTS Banking;
CREATE DATABASE Banking;
USE Banking;

CREATE TABLE employee (
    person_name CHAR(20),
    street CHAR(30),
    city CHAR(30),
    salary INTEGER,
    PRIMARY KEY (person_name)
);

INSERT INTO employee VALUES ('Alice', 'Tianmushan', 'Hangzhou', 8000);
INSERT INTO employee VALUES ('Bob', 'Nanjing', 'Shanghai', 9000);
INSERT INTO employee VALUES ('Charlie', 'Moganshan', 'Hangzhou', 7500);

SELECT * FROM employee;

SHOW GRANTS FOR CURRENT_USER();
