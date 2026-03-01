import os
import joblib
from sklearn.ensemble import RandomForestClassifier

from ml.training.load_training_data import load_training_data
from ml.training.feature_engineering import prepare_features

# Absolute path inside Airflow container
ARTIFACT_PATH = "/opt/airflow/ml/training/artifacts"

def train_model():
    # Ensure artifacts directory exists
    os.makedirs(ARTIFACT_PATH, exist_ok=True)

    # Load & prepare data
    df = load_training_data()
    X_train, X_test, y_train, y_test, scaler = prepare_features(df)

    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    # Save artifacts
    joblib.dump(model, f"{ARTIFACT_PATH}/fraud_model.pkl")
    joblib.dump(scaler, f"{ARTIFACT_PATH}/scaler.pkl")

    print("✅ Model and scaler saved successfully")

if __name__ == "__main__":
    train_model()
