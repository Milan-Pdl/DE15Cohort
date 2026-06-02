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
    
    INSERT INTO gold.daily_transaction_summary(
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
            ON ft.account_id=da.account_id
        JOIN silver.dim_branch db
            ON da.branch_id=db.branch_id
        GROUP BY
        ft.transaction_date::DATE,
        db.branch_name,
        da.account_type,
        ft.transaction_type;
    """
    execute_sql(sql)

def build_gold_360():
    pass

def build_branch_performance_summary():
    pass

def main():
    build_gold_transaction_summary()
    build_gold_360()
    build_branch_performance_summary()

if __name__ == "__main__":
    main()