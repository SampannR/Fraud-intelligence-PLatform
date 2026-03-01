import sys
from pathlib import Path

AIRFLOW_HOME = Path(__file__).resolve().parents[1]
sys.path.append(str(AIRFLOW_HOME))

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from ml.training.train_fraud_model import train_model
from ml.evaluation.evaluate_fraud_model import evaluate_model

default_args = {
    "owner": "airflow",
    "start_date": datetime(2026, 2, 18),
    "retries": 1
}

with DAG(
    dag_id="fraud_model_training",
    schedule_interval="@weekly",
    default_args=default_args,
    catchup=False,
    tags=["fraud", "ml", "training"]
) as dag:

    train = PythonOperator(
        task_id="train_fraud_model",
        python_callable=train_model
    )

    evaluate = PythonOperator(
        task_id="evaluate_fraud_model",
        python_callable=evaluate_model
    )

    train >> evaluate
