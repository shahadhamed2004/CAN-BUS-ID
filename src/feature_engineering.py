import pandas as pd
from pathlib import Path

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"

# 2. Load preprocessed dataset
input_path = results_dir / "processed_DoS_dataset.csv"
data = pd.read_csv(input_path)

print("Dataset loaded:", data.shape)

# 3. Convert CAN ID from hexadecimal to integer
data["CAN_ID"] = data["CAN_ID"].astype(str).apply(
    lambda x: int(x, 16)
)

# 4. Fill missing CAN payload bytes with 0
byte_columns = [
    "Byte_0", "Byte_1", "Byte_2", "Byte_3",
    "Byte_4", "Byte_5", "Byte_6", "Byte_7"
]

data[byte_columns] = data[byte_columns].fillna(0)

# 5. Remove absolute timestamp
data = data.drop(columns=["Timestamp"])

# 6. Ensure numeric data types
for col in ["CAN_ID", "DLC"] + byte_columns:
    data[col] = pd.to_numeric(data[col])

data["Label"] = data["Label"].astype(int)

# 7. Save feature-engineered dataset
output_path = results_dir / "features_DoS_dataset.csv"
data.to_csv(output_path, index=False)

print("\nFEATURE ENGINEERING COMPLETED!")
print("Dataset shape:", data.shape)
print("Missing values:", data.isnull().sum().sum())
print("Labels:", data["Label"].value_counts().to_dict())
print("Saved to:", output_path)