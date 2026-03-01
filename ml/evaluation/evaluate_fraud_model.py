import os
import sys
sys.path.append("/opt/airflow")
import json
import joblib
from sklearn.metrics import classification_report, roc_auc_score
from ml.training.load_training_data import load_training_data
from ml.training.feature_engineering import prepare_features

BASE_PATH = "/opt/airflow"

ARTIFACT_PATH = f"{BASE_PATH}/ml/training/artifacts"
METRICS_DIR = f"{BASE_PATH}/ml/evaluation/metrics"
METRICS_PATH = f"{METRICS_DIR}/metrics.json"

def evaluate_model():

    os.makedirs(METRICS_DIR, exist_ok=True)
    df = load_training_data()
    X_train, X_test, y_train, y_test, _ = prepare_features(df)

    model = joblib.load(f"{ARTIFACT_PATH}/fraud_model.pkl")

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    metrics = {
        "roc_auc": roc_auc_score(y_test, probs),
        "classification_report": classification_report(y_test, preds, output_dict=True)
    }

    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)

    print("Evaluation metrics saved")

if __name__ == "__main__":
    evaluate_model()
