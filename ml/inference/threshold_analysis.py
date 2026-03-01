import json
import numpy as np
from sklearn.metrics import precision_score, recall_score
import joblib
from ml.training.load_training_data import load_training_data
from ml.training.feature_engineering import prepare_features

ARTIFACT_PATH = "ml/training/artifacts/"
OUTPUT_PATH = "ml/evaluation/metrics/threshold_metrics.json"

def evaluate_thresholds():
    df = load_training_data()
    _, X_test, _, y_test, _ = prepare_features(df)

    model = joblib.load(f"{ARTIFACT_PATH}/fraud_model.pkl")
    probs = model.predict_proba(X_test)[:, 1]

    results = {}

    for threshold in np.arange(0.1, 1.0, 0.1):
        preds = (probs >= threshold).astype(int)
        results[str(round(threshold, 2))] = {
            "precision": precision_score(y_test, preds, zero_division=0),
            "recall": recall_score(y_test, preds, zero_division=0)
        }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=4)

    print("📊 Threshold analysis saved")

if __name__ == "__main__":
    evaluate_thresholds()