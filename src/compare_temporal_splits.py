
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"

# 2. Load dataset
data = pd.read_csv(
    results_dir / "processed_DoS_dataset.csv"
)

# 3. Define features and labels
X = data.drop(columns=["Label", "Timestamp", "Section"],
              errors="ignore")
y = data["Label"]

# 4. Random stratified split
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 5. Display class distribution
print("===== STRATIFIED RANDOM SPLIT =====")

print("\nTraining:")
print(y_train.value_counts())

print("\nTesting:")
print(y_test.value_counts())

print("\n===== SPLIT SIZES =====")
print("Training:", len(X_train))
print("Testing:", len(X_test))

print("\nSPLIT COMPARISON COMPLETED!")
