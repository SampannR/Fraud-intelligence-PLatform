import os
import shutil
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def ingest_fraud_data():
    source_path = "/opt/airflow/data_lake/external_source/creditcard.csv"

    if not os.path.exists(source_path):
        raise FileNotFoundError("Source fraud dataset not found")

    ingestion_date = datetime.today().strftime("%Y-%m-%d")

    target_dir = f"data_lake/raw/fraud/ingestion_date={ingestion_date}"
    os.makedirs(target_dir, exist_ok=True)

    target_path = os.path.join(target_dir, "creditcard.csv")

    shutil.copy(source_path, target_path)

    logging.info(f"Fraud data ingested successfully to {target_path}")
