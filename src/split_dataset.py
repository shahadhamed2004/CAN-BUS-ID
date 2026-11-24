import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"

# 2. Load dataset
data = pd.read_csv(results_dir / "features_DoS_dataset.csv")

# 3. Separate features and labels
X = data.drop(columns=["Label"])
y = data["Label"]

# 4. Split dataset (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# 5. Save training and testing datasets
train_data = X_train.copy()
train_data["Label"] = y_train

test_data = X_test.copy()
test_data["Label"] = y_test

train_data.to_csv(results_dir / "train_DoS.csv", index=False)
test_data.to_csv(results_dir / "test_DoS.csv", index=False)

# 6. Results
print("TRAIN/TEST SPLIT COMPLETED!")
print("Training shape:", train_data.shape)
print("Testing shape:", test_data.shape)
print("Training labels:", y_train.value_counts().to_dict())
print("Testing labels:", y_test.value_counts().to_dict())
print("Files saved successfully!")