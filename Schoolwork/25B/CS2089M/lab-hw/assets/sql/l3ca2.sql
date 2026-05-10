USE Banking;

INSERT INTO branch VALUES ('Jianshe', 'Hangzhou', 1000000);
INSERT INTO branch VALUES ('Jiaotong', 'Shanghai', 2000000);
INSERT INTO customer VALUES ('Henry', 'Tianmushan', 'Hangzhou');
INSERT INTO customer VALUES ('Rock', 'Nanjing', 'Hangzhou');
INSERT INTO account VALUES ('A001', 'Jianshe', 5000);
INSERT INTO account VALUES ('A002', 'Jiaotong', 8000);
INSERT INTO depositor VALUES ('Henry', 'A001');
INSERT INTO depositor VALUES ('Rock', 'A002');

SELECT * FROM branch;
SELECT * FROM customer;
SELECT * FROM account;
SELECT * FROM depositor;

INSERT INTO customer VALUES ('Henry', 'Nanjing', 'Shanghai');

INSERT INTO customer (customer_street, customer_city)
VALUES ('SomeStreet', 'SomeCity');
