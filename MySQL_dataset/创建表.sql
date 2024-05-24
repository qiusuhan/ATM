USE atm;
CREATE TABLE accounts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(255) NOT NULL,  -- 注意: 实际应用中应使用哈希密码
    balance DECIMAL(10, 2) NOT NULL DEFAULT 0.00
);