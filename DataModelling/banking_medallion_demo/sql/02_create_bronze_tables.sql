CREATE TABLE bronze.branches_raw (
    branch_id TEXT,
    branch_code TEXT,
    branch_name TEXT,
    city TEXT,
    province TEXT,
    source_file TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bronze.customers_raw (
    customer_id TEXT,
    customer_code TEXT,
    full_name TEXT,
    gender TEXT,
    date_of_birth TEXT,
    email TEXT,
    phone_number TEXT,
    city TEXT,
    kyc_status TEXT,
    created_at TEXT,
    updated_at TEXT,
    source_file TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bronze.accounts_raw (
    account_id TEXT,
    account_number TEXT,
    customer_id TEXT,
    branch_id TEXT,
    account_type TEXT,
    account_status TEXT,
    opened_date TEXT,
    current_balance TEXT,
    source_file TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE bronze.transactions_raw (
    transaction_id TEXT,
    transaction_reference TEXT,
    account_id TEXT,
    transaction_date TEXT,
    transaction_type TEXT,
    amount TEXT,
    currency TEXT,
    channel TEXT,
    merchant_name TEXT,
    created_at TEXT,
    source_file TEXT,
    ingestion_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);