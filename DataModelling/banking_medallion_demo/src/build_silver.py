import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pandas as pd
from pydantic import BaseModel, EmailStr, ValidationError
load_dotenv()

class CustomerModel(BaseModel):
    email: EmailStr

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

def execute_sql(sql):
    with engine.begin() as conn:
        conn.execute(text(sql))





def transform_dim_branch(df: pd.DataFrame) -> pd.DataFrame:
    # branch_id -> integer
    df["branch_id"] = pd.to_numeric(df["branch_id"]).astype(int)

    # branch_code -> uppercase
    df["branch_code"] = (
        df["branch_code"]
        .str.strip()
        .str.upper()
    )

    # Clean and standardize text fields
    for col in ["branch_name", "city", "province"]:
        df[col] = (
            df[col]
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .str.title()
        )

    # Remove duplicates
    df = df.drop_duplicates()

    return df        


def is_valid_email(email):
    try:
        CustomerModel(email=email)
        return True
    except ValidationError:
        return False


def transform_customers(df: pd.DataFrame) -> pd.DataFrame:

    # -------------------------
    # 1. Type conversions
    # -------------------------
    df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")

    df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce").dt.date

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")

    # -------------------------
    # 2. Standardize customer_code
    # -------------------------
    df["customer_code"] = df["customer_code"].astype(str).str.strip().str.upper()

    # -------------------------
    # 3. Clean customer name
    # -------------------------
    df["full_name"] = (
        df["full_name"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    df["full_name"] = df["full_name"].replace(["", "nan", "None"], "Unknown Customer")

    # -------------------------
    # 4. KYC status normalization
    # -------------------------
    df["kyc_status"] = (
        df["kyc_status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "verified": "Verified",
            "pending": "Pending",
            "rejected": "Rejected"
        })
        .fillna("Unknown")
    )

    # -------------------------
    # 5. Email validation flag (Pydantic)
    # -------------------------
    df["is_valid_email"] = df["email"].apply(is_valid_email)

    # -------------------------
    # 6. Handle duplicates (keep latest updated_at)
    # -------------------------
    df = df.sort_values("updated_at")
    df = df.drop_duplicates(subset=["customer_id"], keep="last")

    return df


def transform_dim_account(df: pd.DataFrame) -> pd.DataFrame:

    # -------------------------
    # Type conversions
    # -------------------------
    df["account_id"] = pd.to_numeric(
        df["account_id"],
        errors="coerce"
    ).astype("Int64")

    df["customer_id"] = pd.to_numeric(
        df["customer_id"],
        errors="coerce"
    ).astype("Int64")

    df["branch_id"] = pd.to_numeric(
        df["branch_id"],
        errors="coerce"
    ).astype("Int64")

    df["opened_date"] = pd.to_datetime(
        df["opened_date"],
        errors="coerce"
    ).dt.date

    df["current_balance"] = pd.to_numeric(
        df["current_balance"],
        errors="coerce"
    )

    # -------------------------
    # Standardize account_number
    # -------------------------
    df["account_number"] = (
        df["account_number"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # -------------------------
    # Standardize account_type
    # -------------------------
    df["account_type"] = (
        df["account_type"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "saving": "Savings",
            "savings": "Savings",
            "current": "Current",
            "fixed deposit": "Fixed Deposit"
        })
        .fillna("Unknown")
    )

    # -------------------------
    # Standardize account_status
    # -------------------------
    df["account_status"] = (
        df["account_status"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "active": "Active",
            "inactive": "Inactive",
            "closed": "Closed",
            "dormant": "Dormant"
        })
        .fillna("Unknown")
    )

    # -------------------------
    # Negative balance flag
    # -------------------------
    df["is_negative_balance"] = (
        df["current_balance"] < 0
    )

    # -------------------------
    # Remove duplicates
    # -------------------------
    df = df.drop_duplicates(
          subset=["account_id"],
          keep="last"
      )
    return df




def transform_fact_transaction(
    transactions_df: pd.DataFrame,
    accounts_df: pd.DataFrame
) -> pd.DataFrame:

    # -------------------------
    # Type conversions
    # -------------------------
    transactions_df["transaction_id"] = pd.to_numeric(
        transactions_df["transaction_id"],
        errors="coerce"
    ).astype("Int64")

    transactions_df["account_id"] = pd.to_numeric(
        transactions_df["account_id"],
        errors="coerce"
    ).astype("Int64")

    transactions_df["transaction_date"] = pd.to_datetime(
        transactions_df["transaction_date"],
        errors="coerce"
    )

    transactions_df["created_at"] = pd.to_datetime(
        transactions_df["created_at"],
        errors="coerce"
    )

    transactions_df["amount"] = pd.to_numeric(
        transactions_df["amount"],
        errors="coerce"
    )

    # -------------------------
    # Standardize reference
    # -------------------------
    transactions_df["transaction_reference"] = (
        transactions_df["transaction_reference"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # -------------------------
    # Standardize currency
    # -------------------------
    transactions_df["currency"] = (
        transactions_df["currency"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # -------------------------
    # Standardize channel
    # -------------------------
    transactions_df["channel"] = (
        transactions_df["channel"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
    )

    transactions_df["channel"] = (
        transactions_df["channel"]
        .replace("", "Unknown")
        .str.title()
    )

    # -----------
    # --------------
    # Merchant name
    # --------

    -----------------
    transactions_df["merchant_name"] = (
        transactions_df["merchant_name"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    # -------------------------
    # Standardize transaction type
    # -------------------------
    transactions_df["transaction_type"] = (
        transactions_df["transaction_type"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "deposit": "Deposit",
            "withdrawal": "Withdrawal",
            "transfer": "Transfer",
            "card payment": "Card Payment",
            "fee": "Fee"
        })
        .fillna("Unknown")
    )

    # -------------------------
    # Remove duplicate transactions
    # -------------------------
    transactions_df = transactions_df.drop_duplicates(
        subset=["transaction_id"]
    )

    # -------------------------
    # Data Quality Flag:
    # is_valid_account
    # -------------------------
    valid_accounts = set(
        accounts_df["account_id"]
        .dropna()
        .astype(int)
    )

    transactions_df["is_valid_account"] = (
        transactions_df["account_id"]
        .isin(valid_accounts)
    )

    # -------------------------
    # Data Quality Flag:
    # is_valid_amount
    # -------------------------
    transactions_df["is_valid_amount"] = (
        transactions_df["amount"] > 0
    )

    # -------------------------
    # Data Quality Flag:
    # is_valid_currency
    # -------------------------
    transactions_df["is_valid_currency"] = (
        transactions_df["currency"]
        .isin(["NPR", "USD"])
    )

    return transactions_df



def build_silver_branches(engine):
    df = pd.read_sql(
        "SELECT * FROM bronze.branches_raw",
        con=engine
    )

    df = transform_dim_branch(df)

    df.to_sql(
        name="dim_branch",
        schema="silver",
        con=engine,
        if_exists="append",
        index=False
    )


def build_silver_customers(engine):
    df = pd.read_sql(
        "SELECT * FROM bronze.customers_raw",
        con=engine
    )

    df = transform_customers(df)

    df.to_sql(
        name="dim_customer",
        schema="silver",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} clean customers into silver.dim_customer")



def build_silver_accounts(engine):

    df = pd.read_sql(
        "SELECT * FROM bronze.accounts_raw",
        con=engine
    )

    df = transform_dim_account(df)

    df.to_sql(
        name="dim_account",
        schema="silver",
        con=engine,
        if_exists="append",
        index=False
    )

    print(f"Loaded {len(df)} rows into silver.dim_account")

def build_silver_transactions(engine):
    transactions_df = pd.read_sql(
        "SELECT * FROM bronze.transactions_raw",
        con=engine
    )

    accounts_df = pd.read_sql(
        """
        SELECT account_id
        FROM silver.dim_account
        """,
        con=engine
    )

    transactions_df = transform_fact_transaction(
        transactions_df,
        accounts_df
    )

    transactions_df.to_sql(
        name="fact_transaction",
        schema="silver",
        con=engine,
        if_exists="append",
        index=False
    )

    print(
        f"Loaded {len(transactions_df)} rows "
        f"into silver.fact_transaction"
    )


def main():
    build_silver_branches(engine)
    build_silver_customers(engine)
    build_silver_accounts(engine)
    build_silver_transactions(engine)
    
if __name__ == "__main__":
    main()