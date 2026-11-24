import pandas as pd
import csv
from pathlib import Path
from collections import Counter

# 1. Define project paths
project_dir = Path(__file__).resolve().parents[1]

file_path = project_dir / "dataset" / "9) Car-Hacking Dataset" / "DoS_dataset.csv"
results_dir = project_dir / "results"

results_dir.mkdir(exist_ok=True)

# 2. Load dataset
data = pd.read_csv(file_path, header=None)

print("\n===== DATASET OVERVIEW =====")

# 3. Display first 5 rows
print("\nFirst 5 rows:")
print(data.head())

# 4. Display dataset dimensions
print("\nDataset shape:")
print(data.shape)

# 5. Display data types
print("\nData types:")
print(data.dtypes)

# 6. Check missing values
print("\nMissing values:")
print(data.isnull().sum())

# 7. Basic statistics
print("\nBasic statistics:")
print(data.describe(include="all"))

# 8. Count labels from original CSV rows
label_counts = Counter()

with open(file_path, "r", newline="", encoding="utf-8") as file:
    reader = csv.reader(file)

    for row in reader:
        if row:
            label = row[-1].strip()
            label_counts[label] += 1

print("\nLabel distribution:")
print(label_counts)

# 9. Save analysis results
data.isnull().sum().to_csv(
    results_dir / "missing_values.csv"
)

data.describe(include="all").to_csv(
    results_dir / "basic_statistics.csv"
)

pd.Series(label_counts).to_csv(
    results_dir / "label_distribution.csv"
)

print("\n===== DATASET ANALYSIS COMPLETED =====")
print("All results saved successfully!")
import matplotlib.pyplot as plt

# 10. Label distribution chart
plt.figure(figsize=(8, 5))
pd.Series(label_counts).plot(
    kind="bar",
    title="CAN Message Label Distribution"
)
plt.xlabel("Label")
plt.ylabel("Number of Messages")
plt.tight_layout()
plt.savefig(results_dir / "label_distribution.png")
plt.close()

# 11. Missing values chart
plt.figure(figsize=(10, 5))
data.isnull().sum().plot(
    kind="bar",
    title="Missing Values per Column"
)
plt.xlabel("Columns")
plt.ylabel("Missing Values")
plt.tight_layout()
plt.savefig(results_dir / "missing_values.png")
plt.close()

print("\nCharts saved successfully!")