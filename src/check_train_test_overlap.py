
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

# 3. Stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 4. Hash feature rows
train_hashes = pd.util.hash_pandas_object(
    X_train, index=False
)

test_hashes = pd.util.hash_pandas_object(
    X_test, index=False
)

# 5. Check overlap
overlap = set(train_hashes).intersection(set(test_hashes))

print("===== TRAIN TEST OVERLAP =====")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))
print("Overlapping feature hashes:", len(overlap))
print("Overlap percentage:",
      len(overlap) / len(X_test) * 100)

print("\nOVERLAP CHECK COMPLETED!")
