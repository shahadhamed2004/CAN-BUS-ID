
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_DIR / "results" / "processed_DoS_dataset.csv"
OUTPUT_PATH = PROJECT_DIR / "results" / "feature_diversity.csv"

data = pd.read_csv(DATA_PATH)

features = [
    "CAN_ID", "DLC",
    "Byte_0", "Byte_1", "Byte_2", "Byte_3",
    "Byte_4", "Byte_5", "Byte_6", "Byte_7"
]

results = []

for label in sorted(data["Label"].unique()):

    subset = data[data["Label"] == label]

    row = {
        "Label": label,
        "Total Records": len(subset),
        "Unique Feature Combinations":
            len(subset[features].drop_duplicates())
    }

    for feature in features:
        row[f"{feature} Unique Values"] = subset[feature].nunique()

    results.append(row)

report = pd.DataFrame(results)

report.to_csv(OUTPUT_PATH, index=False)

print("Feature diversity results saved successfully!")
print(report.to_string(index=False))
print("\nSaved at:", OUTPUT_PATH)
