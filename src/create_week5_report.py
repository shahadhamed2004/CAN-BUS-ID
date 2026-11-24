
import pandas as pd
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_DIR / "results"

# Load evaluation results
results = pd.read_csv(
    RESULTS_DIR / "model_evaluation.csv"
)

report_path = RESULTS_DIR / "week5_evaluation_report.txt"

with open(report_path, "w", encoding="utf-8") as file:

    file.write("CAN-BUS-IDS - WEEK 5 EVALUATION REPORT\n")
    file.write("=" * 50 + "\n\n")

    file.write("1. MODEL COMPARISON\n")
    file.write("-" * 50 + "\n")

    file.write(results.to_string(index=False))
    file.write("\n\n")

    file.write("2. CONFUSION MATRIX ANALYSIS\n")
    file.write("-" * 50 + "\n")

    for _, row in results.iterrows():
        file.write(f"\nModel: {row['Model']}\n")
        file.write(f"True Negatives: {row['True Negatives']}\n")
        file.write(f"False Positives: {row['False Positives']}\n")
        file.write(f"False Negatives: {row['False Negatives']}\n")
        file.write(f"True Positives: {row['True Positives']}\n")

    file.write("\n\n3. DATASET LIMITATIONS\n")
    file.write("-" * 50 + "\n")

    file.write(
        "The dataset inspection found that all 587,521 attack "
        "records have the same feature combination.\n"
    )

    file.write(
        "This means the attack class has very limited feature diversity.\n"
    )

    file.write(
        "The random train-test split also contains overlapping "
        "feature combinations.\n"
    )

    file.write(
        "Therefore, the perfect test results do not prove that "
        "the models can detect previously unseen attack patterns.\n"
    )

    file.write(
        "Further testing with more diverse attack data is necessary.\n"
    )

    file.write("\n\n4. FINAL MODEL CHOICE\n")
    file.write("-" * 50 + "\n")

    file.write(
        "Both models achieved identical evaluation results.\n"
    )

    file.write(
        "The Decision Tree is selected provisionally because "
        "it is simpler to interpret and explain.\n"
    )

    file.write(
        "This choice does not demonstrate better detection "
        "performance than Random Forest.\n"
    )

print("Week 5 evaluation report created successfully!")
print("Saved at:", report_path)
