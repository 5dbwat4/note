DROP DATABASE IF EXISTS Banking;
CREATE DATABASE Banking;
USE Banking;

CREATE TABLE customer (
    customer_name CHAR(20),
    customer_street CHAR(30),
    customer_city CHAR(30),
    PRIMARY KEY (customer_name)
);

CREATE TABLE branch (
    branch_name CHAR(15),
    branch_city CHAR(30),
    assets INTEGER,
    PRIMARY KEY (branch_name),
    CHECK (assets >= 0)
);

CREATE TABLE account (
    account_number CHAR(10),
    branch_name CHAR(15),
    balance INTEGER,
    PRIMARY KEY (account_number),
    FOREIGN KEY (branch_name) REFERENCES branch(branch_name)
        ON DELETE RESTRICT
        ON UPDATE RESTRICT,
    CHECK (balance >= 0)
);

CREATE TABLE depositor (
    customer_name CHAR(20),
    account_number CHAR(10),
    PRIMARY KEY (customer_name, account_number),
    FOREIGN KEY (account_number) REFERENCES account(account_number)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (customer_name) REFERENCES customer(customer_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

SHOW TABLES;

SHOW CREATE TABLE branch;
SHOW CREATE TABLE account;
SHOW CREATE TABLE depositor;
