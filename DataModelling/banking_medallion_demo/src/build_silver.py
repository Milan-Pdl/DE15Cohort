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
        
def build_silver_branches():
    sql = """
    INSERT INTO silver.dim_branch(branch_id, branch_code, branch_name, city, province)
    SELECT DISTINCT branch_id::INTEGER, UPPER(TRIM(branch_code)),
    INITCAP(TRIM(branch_name)),
    INITCAP(TRIM(city)),
    INITCAP(TRIM(province))
    FROM bronze.branches_raw
    WHERE branch_id IS NOT NULL;
    """
    execute_sql(sql)

def build_silver_customers():
    pass

def build_silver_accounts():
    pass

def build_silver_transactions():
    pass

def main():
    build_silver_branches()
    build_silver_customers()
    build_silver_accounts()
    build_silver_transactions()
    
if __name__ == "__main__":
    main()