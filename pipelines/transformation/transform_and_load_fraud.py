import os
import pandas as pd
from glob import glob
from sqlalchemy import create_engine, text

RAW_BASE_PATH = "/opt/airflow/data_lake/raw/fraud"
DB_CONN = "postgresql+psycopg2://fraud_admin:fraud_pass@postgres:5432/fraud_warehouse"


def get_latest_raw_file():
    files = sorted(
        glob(f"{RAW_BASE_PATH}/ingestion_date=*/creditcard.csv"),
        reverse=True
    )

    if not files:
        raise FileNotFoundError("No raw fraud data found in data lake")

    return files[0]


def transform_and_load():
    raw_file_path = get_latest_raw_file()
    print(f"Reading raw data from: {raw_file_path}")

    df = pd.read_csv(raw_file_path)

    df["Class"] = (
    df["Class"]
    .astype(str)
    .str.replace("'", "", regex=False)
    .astype(int)
    )       

    # Data quality checks
    df = df.dropna()
    df = df[df["Amount"] >= 0]
    df = df[df["Class"].isin([0, 1])]

    # Feature engineering
    df["transaction_hour"] = (df["Time"] // 3600) % 24
    df["is_high_value"] = df["Amount"] > 2000

    engine = create_engine(DB_CONN)

    # 🔹 Ensure schema exists
    with engine.begin() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS public"))

    # 🔹 Load data (this WILL create the table)
    df.to_sql(
        name="fraud_transactions",
        con=engine,
        schema="public",
        if_exists="replace",
        index=False,
        method="multi",
        chunksize=1000
    )

    print("fraud_transactions table created & data loaded successfully")
