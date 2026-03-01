import sys
sys.path.append("/opt/airflow")

import os
import joblib
import pandas as pd
from datetime import datetime

from ml.training.load_training_data import load_training_data
from ml.training.feature_engineering import prepare_features

# Paths
ARTIFACT_PATH = "/opt/airflow/ml/training/artifacts"
OUTPUT_PATH = "/opt/shared/inference_output"

MODEL_PATH = f"{ARTIFACT_PATH}/fraud_model.pkl"
THRESHOLD = float(os.getenv("FRAUD_THRESHOLD", 0.5))

def assign_risk_band(p):
    if p < 0.3:
        return "low"
    elif p < 0.7:
        return "medium"
    else:
        return "high"

def run_inference():
    print("📥 Loading data for inference...")
    df = load_training_data()

    print(f"Input rows: {len(df)}")

    # Feature engineering (same as training)
    _, X_test, _, _, _ = prepare_features(df)

    print("🤖 Loading trained model...")
    model = joblib.load(MODEL_PATH)

    print("🔮 Generating predictions...")
    probs = model.predict_proba(X_test)[:, 1]
    preds = (probs >= THRESHOLD).astype(int)

    results = pd.DataFrame({
    "fraud_probability": probs,
    "fraud_prediction": preds,
    "risk_band": [assign_risk_band(p) for p in probs]
    })

    # Ensure output directory exists
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    output_file = f"{OUTPUT_PATH}/fraud_predictions_{timestamp}.csv"

    results.to_csv(output_file, index=False)

    print(f"✅ Predictions saved to {output_file}")
    print("Max probability:", probs.max())
    print("Mean probability:", probs.mean())
    print("Top 10 probabilities:", sorted(probs, reverse=True)[:10])

if __name__ == "__main__":
    run_inference()