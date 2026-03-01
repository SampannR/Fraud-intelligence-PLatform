import sys
sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from pipelines.transformation.transform_and_load_fraud import transform_and_load

default_args = {
    "owner": "airflow",
    "retries": 2,
    "retry_delay": timedelta(minutes=2)
}

with DAG(
    dag_id="fraud_data_transformation",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args
) as dag:

    transform_load_task = PythonOperator(
        task_id="transform_and_load_fraud_data",
        python_callable=transform_and_load
    )

    transform_load_task
