import pandas as pd
from sqlalchemy import create_engine

DB_CONN = "postgresql+psycopg2://fraud_admin:fraud_pass@postgres:5432/fraud_warehouse"

def load_training_data():
    engine = create_engine(DB_CONN)
    query = "SELECT * FROM fraud_transactions"
    df = pd.read_sql(query, engine)
    return df
