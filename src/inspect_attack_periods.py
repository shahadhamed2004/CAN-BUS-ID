import pandas as pd
from pathlib import Path

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"

# 2. Load dataset
data = pd.read_csv(
    results_dir / "processed_DoS_dataset.csv"
)

# 3. Check time range for each class
print("===== TIMESTAMP RANGE BY LABEL =====")

for label, group in data.groupby("Label"):
    name = "Normal" if label == 0 else "Attack"

    print(f"\n{name}:")
    print("Records:", len(group))
    print("First timestamp:", group["Timestamp"].min())
    print("Last timestamp:", group["Timestamp"].max())

# 4. Check label transitions
changes = data["Label"].ne(data["Label"].shift())

print("\n===== LABEL TRANSITIONS =====")
print("Number of label transitions:", changes.sum())

# 5. Show first and last records of each period
data["Period"] = changes.cumsum()

periods = data.groupby("Period").agg(
    Label=("Label", "first"),
    Start=("Timestamp", "first"),
    End=("Timestamp", "last"),
    Records=("Label", "size")
)

periods["Class"] = periods["Label"].map({
    0: "Normal",
    1: "Attack"
})

print("\n===== FIRST 20 PERIODS =====")
print(periods.head(20).to_string())

print("\n===== LAST 20 PERIODS =====")
print(periods.tail(20).to_string())

print("\nINSPECTION COMPLETED!")