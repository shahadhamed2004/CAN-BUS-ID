import pandas as pd
import joblib
from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Project paths
project_dir = Path(__file__).resolve().parents[1]
results_dir = project_dir / "results"
models_dir = project_dir / "models"

# 2. Load test dataset
test_data = pd.read_csv(results_dir / "test_DoS.csv")

X_test = test_data.drop(columns=["Label"])
y_test = test_data["Label"]

# 3. Load trained models
model_files = {
    "Decision Tree": "decision_tree.pkl",
    "Random Forest": "random_forest.pkl"
}

all_results = []

# 4. Evaluate each model
for name, filename in model_files.items():

    print("\n==============================")
    print(name)
    print("==============================")

    model = joblib.load(models_dir / filename)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)
    precision = precision_score(y_test, predictions, zero_division=0)
    recall = recall_score(y_test, predictions, zero_division=0)
    f1 = f1_score(y_test, predictions, zero_division=0)

    cm = confusion_matrix(y_test, predictions)

    tn, fp, fn, tp = cm.ravel()

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-Score:", f1)

    print("\nConfusion Matrix:")
    print(cm)

    print("\nFalse Positives:", fp)
    print("False Negatives:", fn)

    print("\nClassification Report:")
    print(classification_report(y_test, predictions))

    all_results.append({
        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "False Positives": fp,
        "False Negatives": fn
    })

# 5. Save evaluation results
results = pd.DataFrame(all_results)

results.to_csv(
    results_dir / "detailed_evaluation.csv",
    index=False
)

print("\nEVALUATION COMPLETED!")
print(results)
print("\nResults saved successfully!")