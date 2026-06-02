CREATE TABLE silver.dim_branch (
    branch_id INTEGER PRIMARY KEY,
    branch_code VARCHAR(20),
    branch_name VARCHAR(150),
    city VARCHAR(100),
    province VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE silver.dim_customer (
    customer_id INTEGER PRIMARY KEY,
    customer_code VARCHAR(30),
    full_name VARCHAR(150),
    gender VARCHAR(20),
    date_of_birth DATE,
    email VARCHAR(150),
    phone_number VARCHAR(100),
    city VARCHAR(100),
    kyc_status VARCHAR(30),
    customer_created_at TIMESTAMP,
    customer_updated_at TIMESTAMP,
    is_valid_email BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE silver.dim_account (
    account_id INTEGER PRIMARY KEY,
    account_number VARCHAR(50),
    customer_id INTEGER,
    branch_id INTEGER,
    account_type VARCHAR(50),
    account_status VARCHAR(50),
    opened_date DATE,
    current_balance NUMERIC(18, 2),
    is_negative_balance BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE silver.fact_transaction (
    transaction_id INTEGER PRIMARY KEY,
    transaction_reference VARCHAR(50),
    account_id INTEGER,
    transaction_date TIMESTAMP,
    transaction_type VARCHAR(50),
    amount NUMERIC(18, 2),
    currency VARCHAR(10),
    channel VARCHAR(50),
    merchant_name VARCHAR(150),
    transaction_created_at TIMESTAMP,
    is_valid_account BOOLEAN,
    is_valid_amount BOOLEAN,
    is_valid_currency BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);