CREATE TABLE gold.daily_transaction_summary (
    transaction_date DATE,
    branch_name VARCHAR(150),
    account_type VARCHAR(50),
    transaction_type VARCHAR(50),
    transaction_count INTEGER,
    total_amount NUMERIC(18, 2),
    average_amount NUMERIC(18, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE gold.customer_360 (
    customer_id INTEGER PRIMARY KEY,
    customer_code VARCHAR(30),
    full_name VARCHAR(150),
    city VARCHAR(100),
    kyc_status VARCHAR(30),
    total_accounts INTEGER,
    active_accounts INTEGER,
    total_balance NUMERIC(18, 2),
    total_transactions INTEGER,
    total_transaction_amount NUMERIC(18, 2),
    last_transaction_date TIMESTAMP,
    customer_segment VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE gold.branch_performance_summary (
    branch_id INTEGER,
    branch_name VARCHAR(150),
    city VARCHAR(100),
    total_customers INTEGER,
    total_accounts INTEGER,
    total_balance NUMERIC(18, 2),
    total_transactions INTEGER,
    total_transaction_amount NUMERIC(18, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);