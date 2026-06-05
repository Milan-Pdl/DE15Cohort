import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
    
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def execute_sql(sql):
    with engine.begin() as conn:
        conn.execute(text(sql))
        

def build_gold_transaction_summary():

    sql = """
    TRUNCATE TABLE gold.daily_transaction_summary;

    INSERT INTO gold.daily_transaction_summary (
        transaction_date,
        branch_name,
        account_type,
        transaction_type,
        transaction_count,
        total_amount,
        average_amount
    )
    SELECT
        ft.transaction_date::DATE AS transaction_date,
        db.branch_name,
        da.account_type,
        ft.transaction_type,
        COUNT(*) AS transaction_count,
        SUM(ft.amount) AS total_amount,
        AVG(ft.amount) AS average_amount
    FROM silver.fact_transaction ft
    JOIN silver.dim_account da
        ON ft.account_id = da.account_id
    JOIN silver.dim_branch db
        ON da.branch_id = db.branch_id
    WHERE
        ft.is_valid_account = TRUE
        AND ft.is_valid_amount = TRUE
        AND ft.is_valid_currency = TRUE
        AND ft.transaction_type <> 'Unknown'
    GROUP BY
        ft.transaction_date::DATE,
        db.branch_name,
        da.account_type,
        ft.transaction_type;
    """
    execute_sql(sql)


def build_gold_360():
    
    sql="""
    TRUNCATE TABLE gold.customer_360;

    INSERT INTO gold.customer_360 (
        customer_id,
    customer_code,    
        full_name,
        city,
        kyc_status,
        total_accounts,
        active_accounts,
        total_balance,
        total_transactions,
        total_transaction_amount,
        last_transaction_date,
        customer_segment
    )

    WITH account_summary AS (
        SELECT
            customer_id,
            COUNT(*) AS total_accounts,

            COUNT(*) FILTER (
                WHERE account_status = 'Active'
            ) AS active_accounts,

            COALESCE(
                SUM(current_balance),
                0
            ) AS total_balance

        FROM silver.dim_account
        GROUP BY customer_id
    ),

    transaction_summary AS (
        SELECT
            da.customer_id,

            COUNT(DISTINCT ft.transaction_id)
                AS total_transactions,

            COALESCE(
                SUM(ft.amount),
                0
            ) AS total_transaction_amount,

            MAX(ft.transaction_date)
                AS last_transaction_date

        FROM silver.fact_transaction ft

        JOIN silver.dim_account da
            ON ft.account_id = da.account_id

        WHERE
            ft.is_valid_account = TRUE
            AND ft.is_valid_amount = TRUE
            AND ft.is_valid_currency = TRUE
            AND ft.transaction_type <> 'Unknown'

        GROUP BY da.customer_id
    )

    SELECT
        dc.customer_id,
        dc.customer_code,

        dc.full_name AS full_name,

        dc.city,

        dc.kyc_status,

        COALESCE(
            acc.total_accounts,
            0
        ) AS total_accounts,

        COALESCE(
            acc.active_accounts,
            0
        ) AS active_accounts,

        COALESCE(
            acc.total_balance,
            0
        ) AS total_balance,

        COALESCE(
            txn.total_transactions,
            0
        ) AS total_transactions,

        COALESCE(
            txn.total_transaction_amount,
            0
        ) AS total_transaction_amount,

        txn.last_transaction_date,

        CASE
            WHEN COALESCE(acc.total_balance, 0) >= 300000
                THEN 'High Value'

            WHEN COALESCE(acc.total_balance, 0) >= 100000
                THEN 'Medium Value'

            ELSE 'Regular'
        END AS customer_segment

    FROM silver.dim_customer dc

    LEFT JOIN account_summary acc
        ON dc.customer_id = acc.customer_id

    LEFT JOIN transaction_summary txn
        ON dc.customer_id = txn.customer_id;

    """
    execute_sql(sql)


def build_branch_performance_summary():
    
    sql="""
        TRUNCATE TABLE gold.branch_performance_summary;

    INSERT INTO gold.branch_performance_summary (
        branch_id,
        branch_name,
        city,
        total_customers,
        total_accounts,
        total_balance,
        total_transactions,
        total_transaction_amount
    )

    WITH account_summary AS (
        SELECT
            branch_id,

            COUNT(DISTINCT customer_id)
                AS total_customers,

            COUNT(*)
                AS total_accounts,

            COALESCE(
                SUM(current_balance),
                0
            ) AS total_balance

        FROM silver.dim_account
        GROUP BY branch_id
    ),

    transaction_summary AS (
        SELECT
            da.branch_id,

            COUNT(DISTINCT ft.transaction_id)
                AS total_transactions,

            COALESCE(
                SUM(ft.amount),
                0
            ) AS total_transaction_amount

        FROM silver.fact_transaction ft

        JOIN silver.dim_account da
            ON ft.account_id = da.account_id

        WHERE
            ft.is_valid_account = TRUE
            AND ft.is_valid_amount = TRUE
            AND ft.is_valid_currency = TRUE
            AND ft.transaction_type <> 'Unknown'

        GROUP BY da.branch_id
    )

    SELECT
        db.branch_id,
        db.branch_name,
        db.city,

        COALESCE(
            acc.total_customers,
            0
        ) AS total_customers,

        COALESCE(
            acc.total_accounts,
            0
        ) AS total_accounts,

        COALESCE(
            acc.total_balance,
            0
        ) AS total_balance,

        COALESCE(
            txn.total_transactions,
            0
        ) AS total_transactions,

        COALESCE(
            txn.total_transaction_amount,
            0
        ) AS total_transaction_amount

    FROM silver.dim_branch db

    LEFT JOIN account_summary acc
        ON db.branch_id = acc.branch_id

    LEFT JOIN transaction_summary txn
        ON db.branch_id = txn.branch_id;
    """
    execute_sql(sql)


def main():
    build_gold_transaction_summary()
    build_gold_360()
    build_branch_performance_summary()

if __name__ == "__main__":
    main()