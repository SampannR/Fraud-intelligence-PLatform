from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys

sys.path.append("/opt/airflow")

from ml.inference.predict_fraud import run_inference

default_args = {
    "owner": "airflow",
    "retries": 1
}

with DAG(
    dag_id="fraud_inference",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    inference_task = PythonOperator(
        task_id="run_fraud_inference",
        python_callable=run_inference
    )

    inference_task