
import pandas as pd
from pathlib import Path

# 1. Load dataset
project_dir = Path(__file__).resolve().parents[1]

data = pd.read_csv(
    project_dir / "results" / "processed_DoS_dataset.csv"
)

# 2. Separate features
X = data.drop(
    columns=["Label", "Timestamp"],
    errors="ignore"
)

# 3. Calculate feature hashes
data["Feature_Hash"] = pd.util.hash_pandas_object(
    X, index=False
).values

# 4. Group identical feature combinations
groups = data.groupby("Feature_Hash").agg(
    Records=("Label", "size"),
    Different_Labels=("Label", "nunique"),
    Normal=("Label", lambda x: (x == 0).sum()),
    Attack=("Label", lambda x: (x == 1).sum())
)

# 5. Identify conflicting labels
conflicts = groups[
    groups["Different_Labels"] > 1
]

# 6. Display results
print("===== DUPLICATE LABEL CONSISTENCY =====")

print("Unique feature combinations:", len(groups))
print("Feature combinations with multiple labels:",
      len(conflicts))

print("Normal and attack records in conflicts:",
      conflicts[["Normal", "Attack"]].sum().to_dict())

print("\nDUPLICATE LABEL INSPECTION COMPLETED!")
