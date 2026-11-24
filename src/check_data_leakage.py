import pandas as pd
from pathlib import Path

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"

# 2. Load datasets
train = pd.read_csv(results_dir / "train_DoS.csv")
test = pd.read_csv(results_dir / "test_DoS.csv")

# 3. Separate features and labels
X_train = train.drop(columns=["Label"])
y_train = train["Label"]

X_test = test.drop(columns=["Label"])
y_test = test["Label"]

# 4. Check identical feature rows
train_hash = pd.util.hash_pandas_object(
    X_train, index=False
)

test_hash = pd.util.hash_pandas_object(
    X_test, index=False
)

# 5. Compare train and test
train_hashes = set(train_hash)

overlap = test_hash.isin(train_hashes)

print("===== DATA OVERLAP CHECK =====")
print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))
print("Identical feature rows in both sets:", overlap.sum())
print("Overlap percentage:", overlap.mean() * 100)

# 6. Check labels of matching rows
train_pairs = pd.DataFrame({
    "Hash": train_hash,
    "Label": y_train
}).drop_duplicates()

test_pairs = pd.DataFrame({
    "Hash": test_hash,
    "Label": y_test
})

merged = test_pairs.merge(
    train_pairs,
    on="Hash",
    suffixes=("_test", "_train")
)

if len(merged) > 0:
    conflicts = (
        merged["Label_test"] != merged["Label_train"]
    ).sum()

    print("Matching rows with conflicting labels:", conflicts)
else:
    print("No matching feature rows found.")

print("\nCHECK COMPLETED!")