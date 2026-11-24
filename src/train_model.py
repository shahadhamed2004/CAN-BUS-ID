import pandas as pd
import joblib
import matplotlib.pyplot as plt

from pathlib import Path

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay,
    confusion_matrix
)

from sklearn.model_selection import train_test_split


# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RESULTS_DIR = PROJECT_DIR / "results"
MODELS_DIR = PROJECT_DIR / "models"

RESULTS_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)


# ==========================================
# 2. LOAD DATASETS
# ==========================================

train_data = pd.read_csv(
    RESULTS_DIR / "train_DoS.csv"
)

test_data = pd.read_csv(
    RESULTS_DIR / "test_DoS.csv"
)

print("Training dataset:", train_data.shape)
print("Testing dataset:", test_data.shape)


# ==========================================
# 3. PREPARE FEATURES AND LABELS
# ==========================================

# Remove only Label.
# Timestamp is already excluded from these CSV files.

X_train = train_data.drop(columns=["Label"])
y_train = train_data["Label"]

X_test = test_data.drop(columns=["Label"])
y_test = test_data["Label"]

# Check feature consistency

if list(X_train.columns) != list(X_test.columns):
    raise ValueError("Training and testing features do not match!")

print("\nFeatures used:")
print(list(X_train.columns))

print("\nNumber of features:", X_train.shape[1])

print("\nTraining label distribution:")
print(y_train.value_counts().sort_index())

print("\nTesting label distribution:")
print(y_test.value_counts().sort_index())

# Check that both classes exist

if y_train.nunique() < 2 or y_test.nunique() < 2:
    raise ValueError(
        "Both Normal and Attack classes must exist "
        "in training and testing data."
    )


# ==========================================
# 4. CREATE TRAINING SAMPLE
# ==========================================

SAMPLE_SIZE = min(500000, len(X_train))

X_sample, _, y_sample, _ = train_test_split(
    X_train,
    y_train,
    train_size=SAMPLE_SIZE,
    random_state=42,
    stratify=y_train
)

print("\nTraining sample:", X_sample.shape)


# ==========================================
# 5. DEFINE MODELS
# ==========================================

models = {

    "Decision Tree": DecisionTreeClassifier(
        max_depth=20,
        random_state=42,
        class_weight="balanced"
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=100,
        max_depth=20,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

}


# ==========================================
# 6. TRAIN AND EVALUATE
# ==========================================

evaluation_results = []

for name, model in models.items():

    print("\n===================================")
    print("Training:", name)
    print("===================================")

    # Train model

    model.fit(X_sample, y_sample)

    # Predict test data

    predictions = model.predict(X_test)

    # Calculate metrics

    accuracy = accuracy_score(y_test, predictions)

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    # Confusion matrix values

    tn, fp, fn, tp = confusion_matrix(
        y_test,
        predictions,
        labels=[0, 1]
    ).ravel()

    # Print results

    print("\nAccuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-Score:", f1)

    print("\nTrue Negatives:", tn)
    print("False Positives:", fp)
    print("False Negatives:", fn)
    print("True Positives:", tp)

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            labels=[0, 1],
            target_names=["Normal", "Attack"],
            zero_division=0
        )
    )

    # ======================================
    # 7. SAVE MODEL
    # ======================================

    model_filename = (
        name.lower().replace(" ", "_") + ".pkl"
    )

    joblib.dump(
        model,
        MODELS_DIR / model_filename
    )

    # ======================================
    # 8. SAVE CONFUSION MATRIX
    # ======================================

    ConfusionMatrixDisplay.from_predictions(
        y_test,
        predictions,
        labels=[0, 1],
        display_labels=["Normal", "Attack"],
        cmap="Blues"
    )

    plt.title(name + " Confusion Matrix")
    plt.tight_layout()

    chart_name = name.lower().replace(" ", "_")

    plt.savefig(
        RESULTS_DIR / f"{chart_name}_confusion_matrix.png"
    )

    plt.close()

    # ======================================
    # 9. COLLECT RESULTS
    # ======================================

    evaluation_results.append({

        "Model": name,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1-Score": f1,
        "True Negatives": tn,
        "False Positives": fp,
        "False Negatives": fn,
        "True Positives": tp

    })


# ==========================================
# 10. SAVE EVALUATION TABLE
# ==========================================

results = pd.DataFrame(evaluation_results)

results.to_csv(
    RESULTS_DIR / "model_evaluation.csv",
    index=False
)


# ==========================================
# 11. FINAL RESULTS
# ==========================================

print("\n===================================")
print("MODEL TRAINING COMPLETED")
print("===================================")

print("\nFinal Evaluation Results:")

print(results.to_string(index=False))

print("\nModels saved in:", MODELS_DIR)
print("Results saved in:", RESULTS_DIR)

print("\nAll tasks completed successfully!")
