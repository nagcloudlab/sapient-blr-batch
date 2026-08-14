-- ============================================
-- MTS - Money Transfer System Database Schema
-- Production-grade schema with constraints
-- ============================================

CREATE DATABASE IF NOT EXISTS mts_prod;
USE mts_prod;

-- Users table
CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- Accounts table
CREATE TABLE accounts (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    account_number VARCHAR(20) NOT NULL UNIQUE,
    user_id BIGINT NOT NULL,
    account_type ENUM('SAVINGS', 'CURRENT') NOT NULL DEFAULT 'SAVINGS',
    balance DECIMAL(15, 2) NOT NULL DEFAULT 0.00,
    currency VARCHAR(3) NOT NULL DEFAULT 'INR',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_account_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT chk_balance_non_negative CHECK (balance >= 0),
    INDEX idx_account_number (account_number),
    INDEX idx_user_id (user_id)
);

-- Transactions table
CREATE TABLE transactions (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    reference_id VARCHAR(36) NOT NULL UNIQUE,
    from_account_id BIGINT NOT NULL,
    to_account_id BIGINT NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    currency VARCHAR(3) NOT NULL DEFAULT 'INR',
    transfer_mode ENUM('UPI', 'NEFT', 'IMPS', 'RTGS') NOT NULL,
    status ENUM('PENDING', 'SUCCESS', 'FAILED', 'REVERSED') NOT NULL DEFAULT 'PENDING',
    description VARCHAR(255),
    failure_reason VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    CONSTRAINT fk_txn_from_account FOREIGN KEY (from_account_id) REFERENCES accounts(id),
    CONSTRAINT fk_txn_to_account FOREIGN KEY (to_account_id) REFERENCES accounts(id),
    CONSTRAINT chk_amount_positive CHECK (amount > 0),
    CONSTRAINT chk_different_accounts CHECK (from_account_id != to_account_id),
    INDEX idx_reference_id (reference_id),
    INDEX idx_from_account (from_account_id),
    INDEX idx_to_account (to_account_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- Seed data
INSERT INTO users (username, email, password_hash, full_name, phone) VALUES
('ravi.kumar', 'ravi@example.com', '$2a$10$dummyhash1', 'Ravi Kumar', '9876543210'),
('priya.sharma', 'priya@example.com', '$2a$10$dummyhash2', 'Priya Sharma', '9876543211'),
('amit.patel', 'amit@example.com', '$2a$10$dummyhash3', 'Amit Patel', '9876543212');

INSERT INTO accounts (account_number, user_id, account_type, balance) VALUES
('ACC001', 1, 'SAVINGS', 50000.00),
('ACC002', 1, 'CURRENT', 120000.00),
('ACC003', 2, 'SAVINGS', 75000.00),
('ACC004', 3, 'SAVINGS', 30000.00),
('ACC005', 3, 'CURRENT', 200000.00);
