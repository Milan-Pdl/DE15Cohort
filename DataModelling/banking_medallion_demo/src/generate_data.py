import os
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker

fake = Faker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

os.makedirs(DATA_DIR, exist_ok=True)


def generate_branches():
    branches = [
        {
            "branch_id": 1,
            "branch_code": "KTM001",
            "branch_name": "Kathmandu Main Branch",
            "city": "Kathmandu",
            "province": "Bagmati",
        },
        {
            "branch_id": 2,
            "branch_code": "LTP001",
            "branch_name": "Lalitpur Branch",
            "city": "Lalitpur",
            "province": "Bagmati",
        },
        {
            "branch_id": 3,
            "branch_code": "PKR001",
            "branch_name": "Pokhara Branch",
            "city": "Pokhara",
            "province": "Gandaki",
        },
        {
            "branch_id": 4,
            "branch_code": "BRT001",
            "branch_name": "Biratnagar Branch",
            "city": "Biratnagar",
            "province": "Koshi",
        },
    ]

    df = pd.DataFrame(branches)
    df.to_csv(os.path.join(DATA_DIR, "branches.csv"), index=False)


def generate_customers(total_customers=1000):
    customers = []

    for customer_id in range(1, total_customers + 1):
        created_date = fake.date_between(start_date="-5y", end_date="-30d")

        customers.append(
            {
                "customer_id": customer_id,
                "customer_code": f"CUST{customer_id:05d}",
                "full_name": fake.name(),
                "gender": random.choice(["Male", "Female", "Other", None]),
                "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=75),
                "email": fake.email() if random.random() > 0.08 else None,
                "phone_number": fake.phone_number(),
                "city": random.choice(["Kathmandu", "Lalitpur", "Pokhara", "Biratnagar", "Butwal"]),
                "kyc_status": random.choice(["Verified", "Pending", "Rejected", "verified", "pending"]),
                "created_at": created_date,
                "updated_at": created_date + timedelta(days=random.randint(1, 500)),
            }
        )

    df = pd.DataFrame(customers)

    # Introduce duplicate and dirty data intentionally
    duplicate_row = df.iloc[5].copy()
    df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)

    df.loc[3, "email"] = "invalid_email"
    df.loc[10, "full_name"] = None
    df.loc[20, "kyc_status"] = "UNKNOWN"

    df.to_csv(os.path.join(DATA_DIR, "customers.csv"), index=False)


def generate_accounts(total_accounts=14000):
    accounts = []

    for account_id in range(1, total_accounts + 1):
        customer_id = random.randint(1, 100)
        opened_date = fake.date_between(start_date="-4y", end_date="-10d")

        accounts.append(
            {
                "account_id": account_id,
                "account_number": f"AC{account_id:08d}",
                "customer_id": customer_id,
                "branch_id": random.randint(1, 4),
                "account_type": random.choice(["Savings", "Current", "Fixed Deposit", "saving", "CURRENT"]),
                "account_status": random.choice(["Active", "Inactive", "Closed", "Dormant", "active"]),
                "opened_date": opened_date,
                "current_balance": round(random.uniform(500, 500000), 2),
            }
        )

    df = pd.DataFrame(accounts)

    # Dirty data
    df.loc[4, "current_balance"] = -5000
    df.loc[8, "account_type"] = "UnknownType"

    df.to_csv(os.path.join(DATA_DIR, "accounts.csv"), index=False)


def generate_transactions(total_transactions=100000):
    transactions = []

    transaction_types = ["Deposit", "Withdrawal", "Transfer", "Card Payment", "Fee", "deposit", "withdrawal"]
    channels = ["ATM", "Mobile Banking", "Branch", "Internet Banking", "POS", None]

    for transaction_id in range(1, total_transactions + 1):
        transaction_date = fake.date_time_between(start_date="-180d", end_date="now")

        transaction_type = random.choice(transaction_types)

        if transaction_type.lower() in ["deposit"]:
            amount = round(random.uniform(1000, 100000), 2)
        elif transaction_type.lower() in ["withdrawal", "card payment", "fee"]:
            amount = round(random.uniform(100, 50000), 2)
        else:
            amount = round(random.uniform(500, 150000), 2)

        transactions.append(
            {
                "transaction_id": transaction_id,
                "transaction_reference": f"TXN{transaction_id:010d}",
                "account_id": random.randint(1, 140),
                "transaction_date": transaction_date,
                "transaction_type": transaction_type,
                "amount": amount,
                "currency": random.choice(["NPR", "USD", "npr"]),
                "channel": random.choice(channels),
                "merchant_name": random.choice(["Daraz", "Bhatbhateni", "Esewa", "Khalti", "ATM Cash", None]),
                "created_at": transaction_date + timedelta(minutes=random.randint(1, 60)),
            }
        )

    df = pd.DataFrame(transactions)

    # Intentional data quality issues
    df.loc[2, "amount"] = -100
    df.loc[15, "currency"] = "XYZ"
    df.loc[25, "transaction_type"] = "InvalidTxnType"
    df.loc[35, "account_id"] = 9999

    duplicate_row = df.iloc[50].copy()
    df = pd.concat([df, pd.DataFrame([duplicate_row])], ignore_index=True)

    df.to_csv(os.path.join(DATA_DIR, "transactions.csv"), index=False)


if __name__ == "__main__":
    generate_branches()
    generate_customers()
    generate_accounts()
    generate_transactions()

    print("Sample banking CSV files generated successfully.")