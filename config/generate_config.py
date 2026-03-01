import yaml
import os

config = {
    "project": {
        "name": "AI Financial Risk & Fraud Intelligence Platform",
        "environment": "local"
    },
    "data_lake": {
        "raw_path": "data_lake/raw/",
        "processed_path": "data_lake/processed/",
        "features_path": "data_lake/features/"
    },
    "database": {
        "type": "sqlite",
        "name": "fraud_warehouse.db",
        "path": "warehouse/"
    },
    "ml": {
        "model_type": "isolation_forest",
        "contamination": 0.02,
        "random_state": 42
    },
    "llm": {
        "provider": "local",
        "model": "llama3"
    },
    "logging": {
        "level": "INFO"
    }
}

os.makedirs("config", exist_ok=True)

with open("config/config.yaml", "w") as file:
    yaml.dump(config, file, default_flow_style=False)

print("config.yaml generated successfully.")
