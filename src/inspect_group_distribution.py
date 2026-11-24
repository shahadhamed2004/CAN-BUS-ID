
import pandas as pd
from pathlib import Path

# ==========================================
# 1. Load dataset
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_DIR / "results" / "processed_DoS_dataset.csv"

data = pd.read_csv(DATASET_PATH)

print("Dataset loaded:", data.shape)

# ==========================================
# 2. Create feature groups
# ==========================================

X = data.drop(columns=["Label", "Timestamp"])

data["Feature_Hash"] = pd.util.hash_pandas_object(
    X,
    index=False
).values

# ==========================================
# 3. Analyze group labels
# ==========================================

groups = data.groupby("Feature_Hash").agg(
    Records=("Label", "size"),
    Labels=("Label", "nunique"),
    Normal=("Label", lambda x: (x == 0).sum()),
    Attack=("Label", lambda x: (x == 1).sum())
)

normal_groups = groups[groups["Normal"] > 0]
attack_groups = groups[groups["Attack"] > 0]

print("\n===== GROUP DISTRIBUTION =====")

print("Total unique groups:", len(groups))
print("Groups containing Normal:", len(normal_groups))
print("Groups containing Attack:", len(attack_groups))

print("\n===== GROUP SIZES =====")

print("\nAll groups:")
print(groups["Records"].describe())

print("\nNormal groups:")
print(normal_groups["Records"].describe())

print("\nAttack groups:")
print(attack_groups["Records"].describe())

print("\n===== GROUP LABEL CHECK =====")

print("Groups with multiple labels:", (groups["Labels"] > 1).sum())

print("\n===== INSPECTION COMPLETED =====")
