USE Banking;

CREATE TABLE account_audit_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    account_number CHAR(10),
    action VARCHAR(20),
    old_balance INTEGER,
    new_balance INTEGER,
    change_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

DELIMITER //

CREATE TRIGGER trg_account_balance_update
AFTER UPDATE ON account
FOR EACH ROW
BEGIN
    IF OLD.balance != NEW.balance THEN
        INSERT INTO account_audit_log (account_number, action, old_balance, new_balance)
        VALUES (NEW.account_number, 'UPDATE', OLD.balance, NEW.balance);
    END IF;
END //

DELIMITER ;

SHOW TRIGGERS;

UPDATE account SET balance = 6000 WHERE account_number = 'A001';

SELECT * FROM account_audit_log;
