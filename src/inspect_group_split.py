
import pandas as pd
from pathlib import Path
from sklearn.model_selection import StratifiedGroupKFold

# ==========================================
# 1. Load dataset
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "results" / "processed_DoS_dataset.csv"

data = pd.read_csv(DATASET_PATH)

print("Dataset loaded:", data.shape)

# ==========================================
# 2. Prepare features and labels
# ==========================================

X = data.drop(columns=["Label", "Timestamp"])
y = data["Label"]

# ==========================================
# 3. Create groups using feature combinations
# ==========================================

groups = pd.util.hash_pandas_object(
    X,
    index=False
).values

print("\nUnique feature groups:", len(set(groups)))

# ==========================================
# 4. Create stratified group split
# ==========================================

splitter = StratifiedGroupKFold(
    n_splits=5,
    shuffle=True,
    random_state=42
)

train_index, test_index = next(
    splitter.split(X, y, groups)
)

X_train = X.iloc[train_index]
X_test = X.iloc[test_index]

y_train = y.iloc[train_index]
y_test = y.iloc[test_index]

train_groups = set(groups[train_index])
test_groups = set(groups[test_index])

# ==========================================
# 5. Display results
# ==========================================

print("\n===== GROUP SPLIT INSPECTION =====")

print("\nTraining records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining labels:")
print(y_train.value_counts().sort_index())

print("\nTesting labels:")
print(y_test.value_counts().sort_index())

print("\nTraining attack percentage:")
print(round((y_train == 1).mean() * 100, 2), "%")

print("\nTesting attack percentage:")
print(round((y_test == 1).mean() * 100, 2), "%")

# ==========================================
# 6. Check group overlap
# ==========================================

overlap = train_groups.intersection(test_groups)

print("\n===== GROUP OVERLAP CHECK =====")

print("Overlapping groups:", len(overlap))

if len(overlap) == 0:
    print("PASS: No identical feature groups in both sets.")
else:
    print("WARNING: Feature groups overlap!")

# ==========================================
# 7. Final result
# ==========================================

print("\n===== INSPECTION COMPLETED =====")
