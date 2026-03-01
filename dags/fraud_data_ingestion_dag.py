import sys
sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from pipelines.ingestion.ingest_fraud_data import ingest_fraud_data

default_args = {
    "owner": "airflow",
    "retries": 3,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="fraud_data_ingestion",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["fraud", "ingestion", "data_lake"],
) as dag:

    ingest_fraud_csv = PythonOperator(
        task_id="ingest_fraud_csv_to_raw_zone",
        python_callable=ingest_fraud_data,
    )
