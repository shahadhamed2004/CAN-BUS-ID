
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_DIR / "results" / "processed_DoS_dataset.csv"

data = pd.read_csv(DATA_PATH)

features = [
    "CAN_ID",
    "DLC",
    "Byte_0",
    "Byte_1",
    "Byte_2",
    "Byte_3",
    "Byte_4",
    "Byte_5",
    "Byte_6",
    "Byte_7"
]

print("===== FEATURE DIVERSITY ANALYSIS =====")

for label in data["Label"].unique():

    subset = data[data["Label"] == label]

    unique_combinations = subset[features].drop_duplicates()

    print("\nClass:", label)
    print("Total records:", len(subset))
    print("Unique feature combinations:", len(unique_combinations))

    print("\nUnique values per feature:")

    for feature in features:
        print(
            feature,
            ":",
            subset[feature].nunique()
        )

print("\nAnalysis completed!")
