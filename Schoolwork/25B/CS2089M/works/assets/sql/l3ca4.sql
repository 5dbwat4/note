USE Banking;

SELECT * FROM account WHERE branch_name = 'Jiaotong';

UPDATE branch SET branch_name = 'Guangda'
WHERE branch_name = 'Jiaotong';

SELECT * FROM branch;
