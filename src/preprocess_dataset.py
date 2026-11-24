import pandas as pd
import csv
from pathlib import Path

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]

dataset_dir = project_dir / "dataset" / "9) Car-Hacking Dataset"
results_dir = project_dir / "results"

# 2. Dataset file
file_path = dataset_dir / "DoS_dataset.csv"

# 3. Define column names
columns = [
    "Timestamp",
    "CAN_ID",
    "DLC",
    "Byte_0",
    "Byte_1",
    "Byte_2",
    "Byte_3",
    "Byte_4",
    "Byte_5",
    "Byte_6",
    "Byte_7",
    "Label"
]

# 4. Read and normalize variable-length CAN records
records = []

with open(file_path, "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        if not row:
            continue

        dlc = int(row[2])

        if len(row) != 4 + dlc or dlc > 8:
            raise ValueError(f"Invalid CAN record: {row}")

        payload = row[3:3 + dlc]
        label = row[-1].strip()

        records.append(
            [row[0], row[1], dlc]
            + payload
            + [None] * (8 - dlc)
            + [label]
        )

# 5. Create DataFrame
data = pd.DataFrame(records, columns=columns)

# 6. Convert data types
data["Timestamp"] = pd.to_numeric(data["Timestamp"])
data["DLC"] = pd.to_numeric(data["DLC"])

for col in columns[3:11]:
    data[col] = pd.to_numeric(data[col], errors="coerce")

# 7. Encode labels
data["Label"] = data["Label"].map({
    "R": 0,
    "T": 1
})

if data["Label"].isnull().any():
    raise ValueError("Unknown labels found!")

# 8. Save processed dataset
output_path = results_dir / "processed_DoS_dataset.csv"
data.to_csv(output_path, index=False)

print("PREPROCESSING COMPLETED!")
print("Dataset shape:", data.shape)
print("Missing values:", data.isnull().sum().sum())
print("Labels:", data["Label"].value_counts().to_dict())
print("Saved to:", output_path)