
import pandas as pd
from pathlib import Path

# 1. Load dataset
project_dir = Path(__file__).resolve().parents[1]

data = pd.read_csv(
    project_dir / "results" / "processed_DoS_dataset.csv"
)

# 2. Separate features and labels
X = data.drop(
    columns=["Label", "Timestamp"],
    errors="ignore"
)

# 3. Count duplicate feature rows
duplicate_count = X.duplicated().sum()

# 4. Count unique feature rows
unique_count = len(X.drop_duplicates())

# 5. Display results
print("===== DUPLICATE FEATURE ANALYSIS =====")

print("Total records:", len(X))
print("Unique feature rows:", unique_count)
print("Duplicate records:", duplicate_count)

print(
    "Duplicate percentage:",
    round(duplicate_count / len(X) * 100, 2),
    "%"
)

print("\nDUPLICATE FEATURE INSPECTION COMPLETED!")
