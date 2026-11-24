
import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# 1. Load dataset
project_dir = Path(__file__).resolve().parents[1]

data = pd.read_csv(
    project_dir / "results" / "processed_DoS_dataset.csv"
)

# 2. Separate features and labels
X = data.drop(columns=["Label", "Timestamp"], errors="ignore")
y = data["Label"]

# 3. Reproduce the same split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Calculate feature hashes
train_hashes = pd.util.hash_pandas_object(
    X_train, index=False
)

test_hashes = pd.util.hash_pandas_object(
    X_test, index=False
)

# 5. Combine hashes with labels
train_data = pd.DataFrame({
    "Hash": train_hashes.to_numpy(),
    "Label": y_train.to_numpy()
}).drop_duplicates()

test_data = pd.DataFrame({
    "Hash": test_hashes.to_numpy(),
    "Label": y_test.to_numpy()
}).drop_duplicates()

# 6. Compare overlapping features and labels
comparison = train_data.merge(
    test_data,
    on="Hash",
    suffixes=("_Train", "_Test")
)

# 7. Count label differences
different_labels = comparison[
    comparison["Label_Train"] != comparison["Label_Test"]
]

print("===== OVERLAP LABEL ANALYSIS =====")
print("Shared feature-label combinations:", len(comparison))
print("Different label combinations:", len(different_labels))

print("\n===== LABEL COMPARISON =====")
print(comparison.groupby(
    ["Label_Train", "Label_Test"]
).size())

print("\nOVERLAP LABEL INSPECTION COMPLETED!")
