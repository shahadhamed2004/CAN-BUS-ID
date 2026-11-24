
from pathlib import Path
import pandas as pd
import sys

# ==========================================
# 1. Find project directory
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parent.parent

print("Project directory:", PROJECT_DIR)

# ==========================================
# 2. Find processed dataset
# ==========================================

DATASET_NAME = "processed_DoS_dataset.csv"

DATASET_PATH = PROJECT_DIR / "results" / DATASET_NAME

if not DATASET_PATH.exists():
    print("\nDataset not found at:", DATASET_PATH)
    print("\nSearching for the file in the project...")

    matches = [
        path for path in PROJECT_DIR.rglob(DATASET_NAME)
        if ".venv" not in path.parts
    ]

    if matches:
        DATASET_PATH = matches[0]
        print("Dataset found:", DATASET_PATH)
    else:
        print("\nERROR: Dataset file was not found.")

        print("\nCSV files in dataset/ and results/:")
        for folder_name in ["dataset", "results"]:
            folder = PROJECT_DIR / folder_name

            if folder.exists():
                for csv_file in folder.glob("*.csv"):
                    print(csv_file)

        sys.exit(1)

# ==========================================
# 3. Load dataset
# ==========================================

data = pd.read_csv(DATASET_PATH)

print("\nDataset loaded successfully!")
print("Dataset shape:", data.shape)

# ==========================================
# 4. Check required columns
# ==========================================

required_columns = ["Timestamp", "Label"]

for column in required_columns:
    if column not in data.columns:
        raise ValueError(f"Missing required column: {column}")

# ==========================================
# 5. Prepare timestamps
# ==========================================

data["Timestamp"] = pd.to_numeric(
    data["Timestamp"],
    errors="coerce"
)

data = data.dropna(subset=["Timestamp", "Label"])

data = data.sort_values(
    by="Timestamp"
).reset_index(drop=True)

# ==========================================
# 6. Create chronological 80/20 split
# ==========================================

split_index = int(len(data) * 0.8)

train_data = data.iloc[:split_index].copy()
test_data = data.iloc[split_index:].copy()

# ==========================================
# 7. Display results
# ==========================================

print("\n===== TEMPORAL SPLIT INSPECTION =====")

print("\nTotal records:", len(data))
print("Training records:", len(train_data))
print("Testing records:", len(test_data))

print("\nTraining timestamp range:")
print(
    train_data["Timestamp"].min(),
    "-",
    train_data["Timestamp"].max()
)

print("\nTesting timestamp range:")
print(
    test_data["Timestamp"].min(),
    "-",
    test_data["Timestamp"].max()
)

print("\nTraining label distribution:")
print(train_data["Label"].value_counts().sort_index())

print("\nTesting label distribution:")
print(test_data["Label"].value_counts().sort_index())

print("\nTraining attack percentage:")
print(
    round((train_data["Label"] == 1).mean() * 100, 2),
    "%"
)

print("\nTesting attack percentage:")
print(
    round((test_data["Label"] == 1).mean() * 100, 2),
    "%"
)

# ==========================================
# 8. Check chronological separation
# ==========================================

print("\n===== CHRONOLOGICAL CHECK =====")

if train_data["Timestamp"].max() <= test_data["Timestamp"].min():
    print("PASS: Training data comes before testing data.")
else:
    print("WARNING: Training and testing timestamps overlap.")

print("\n===== INSPECTION COMPLETED =====")
