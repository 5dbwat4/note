USE Banking;

INSERT INTO account VALUES ('A003', 'Jianshe', -10);

UPDATE account SET balance = -100 WHERE account_number = 'A001';

INSERT INTO account VALUES ('A003', 'NonExistent', 500);
