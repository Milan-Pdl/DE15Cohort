import os
from dotenv import load_dotenv

import pandas as pd
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def load_csv_to_bronze(file_name,table_name):
    file_path = os.path.join(DATA_DIR, file_name)
    df = pd.read_csv(file_path, dtype=str)
    
    df["source_file"] = file_name
    
    df.to_sql(
        name=table_name,
        con=engine,
        schema="bronze",
        if_exists="append",
        index=False
    )

def main():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE bronze.branches_raw"))
        conn.execute(text("TRUNCATE TABLE bronze.customers_raw"))
        conn.execute(text("TRUNCATE TABLE bronze.accounts_raw"))
        conn.execute(text("TRUNCATE TABLE bronze.transactions_raw"))
    
    load_csv_to_bronze("branches.csv", "branches_raw")
    load_csv_to_bronze("customers.csv", "customers_raw")
    load_csv_to_bronze("accounts.csv", "accounts_raw")
    load_csv_to_bronze("transactions.csv", "transactions_raw")

if __name__ == "__main__":
    main()
