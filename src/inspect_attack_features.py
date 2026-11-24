
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "results" / "processed_DoS_dataset.csv"

data = pd.read_csv(DATASET_PATH)

# Select attack records
attack_data = data[data["Label"] == 1]

# Exclude label and timestamp
attack_features = attack_data.drop(
    columns=["Label", "Timestamp"]
)

print("===== ATTACK FEATURE INSPECTION =====")

print("\nAttack records:", len(attack_data))

print("\nNumber of unique values per feature:")
print(attack_features.nunique())

print("\nFirst 10 attack feature records:")
print(attack_features.head(10).to_string(index=False))

print("\n===== INSPECTION COMPLETED =====")
