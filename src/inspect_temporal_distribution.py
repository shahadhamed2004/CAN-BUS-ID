import pandas as pd
from pathlib import Path

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"

# 2. Load original processed data
data = pd.read_csv(
    results_dir / "processed_DoS_dataset.csv"
)

# 3. Check timestamps
print("===== TIMESTAMP CHECK =====")
print("Dataset rows:", len(data))
print("Timestamp minimum:", data["Timestamp"].min())
print("Timestamp maximum:", data["Timestamp"].max())

print(
    "Timestamps sorted:",
    data["Timestamp"].is_monotonic_increasing
)

# 4. Divide data into 10 sequential sections
data["Section"] = pd.qcut(
    range(len(data)),
    q=10,
    labels=False
)

print("\n===== LABEL DISTRIBUTION BY SECTION =====")

distribution = pd.crosstab(
    data["Section"],
    data["Label"]
)

distribution.columns = [
    "Normal" if col == 0 else "Attack"
    for col in distribution.columns
]

distribution["Total"] = distribution.sum(axis=1)

print(distribution)

# 5. Check attack percentage
print("\n===== ATTACK PERCENTAGE =====")

for section, group in data.groupby("Section"):
    attack_percentage = (
        group["Label"].mean() * 100
    )

    print(
        f"Section {section + 1}: "
        f"{attack_percentage:.2f}% attacks"
    )

print("\nTEMPORAL INSPECTION COMPLETED!")


# 10. Inspect timestamp boundaries of each section

print("\n===== TIMESTAMP BOUNDARIES BY SECTION =====")

for section, group in data.groupby("Section"):
    print(f"\nSection {section + 1}")
    print("Start:", group["Timestamp"].min())
    print("End:", group["Timestamp"].max())
    print("Normal:", (group["Label"] == 0).sum())
    print("Attack:", (group["Label"] == 1).sum())

print("\nSECTION BOUNDARY INSPECTION COMPLETED!")
