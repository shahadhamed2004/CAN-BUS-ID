
import streamlit as st
import pandas as pd
import joblib

from pathlib import Path

# --------------------------------------------------
# PATHS AND SETTINGS
# --------------------------------------------------

PROJECT_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_DIR / "results"
MODELS_DIR = PROJECT_DIR / "models"

MODEL_PATH = MODELS_DIR / "decision_tree.pkl"

FEATURE_COLUMNS = [
    "CAN_ID",
    "DLC",
    "Byte_0",
    "Byte_1",
    "Byte_2",
    "Byte_3",
    "Byte_4",
    "Byte_5",
    "Byte_6",
    "Byte_7"
]

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CAN-BUS-IDS Dashboard",
    page_icon="🚗",
    layout="wide"
)

st.title("CAN-BUS Intrusion Detection System")

st.write(
    "Machine Learning-Based Intrusion Detection "
    "for Automotive CAN Bus Networks"
)

st.divider()

# --------------------------------------------------
# 1. PROJECT INFORMATION
# --------------------------------------------------

st.header("1. Project Information")

col1, col2, col3 = st.columns(3)

col1.metric("Project", "CAN-BUS-IDS")
col2.metric("Machine Learning Models", "2")
col3.metric("Dataset", "HCRL DoS")

st.divider()

# --------------------------------------------------
# 2. DATASET OVERVIEW
# --------------------------------------------------

st.header("2. Dataset Overview")

diversity_path = RESULTS_DIR / "feature_diversity.csv"

if diversity_path.exists():

    diversity = pd.read_csv(diversity_path)

    st.dataframe(diversity, use_container_width=True)

    total_records = diversity["Total Records"].sum()

    attack_rows = diversity[diversity["Label"] == 1]

    unique_attack_combinations = int(
        attack_rows["Unique Feature Combinations"].iloc[0]
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Records",
        f"{total_records:,}"
    )

    col2.metric(
        "Unique Attack Combinations",
        unique_attack_combinations
    )

else:
    st.warning("Feature diversity file not found.")

st.divider()

# --------------------------------------------------
# 3. MODEL EVALUATION
# --------------------------------------------------

st.header("3. Model Evaluation")

evaluation_path = RESULTS_DIR / "model_evaluation.csv"

if evaluation_path.exists():

    evaluation = pd.read_csv(evaluation_path)

    st.dataframe(evaluation, use_container_width=True)

    st.subheader("Model Performance")

    metrics = [
        "Accuracy",
        "Precision",
        "Recall",
        "F1-Score"
    ]

    if all(column in evaluation.columns for column in metrics):
        st.bar_chart(
            evaluation.set_index("Model")[metrics]
        )

else:
    st.warning("Model evaluation file not found.")

st.divider()

# --------------------------------------------------
# 4. CONFUSION MATRICES
# --------------------------------------------------

st.header("4. Confusion Matrices")

col1, col2 = st.columns(2)

decision_tree_image = (
    RESULTS_DIR / "decision_tree_confusion_matrix.png"
)

random_forest_image = (
    RESULTS_DIR / "random_forest_confusion_matrix.png"
)

with col1:

    st.subheader("Decision Tree")

    if decision_tree_image.exists():
        st.image(
            str(decision_tree_image),
            use_container_width=True
        )
    else:
        st.warning("Decision Tree image not found.")

with col2:

    st.subheader("Random Forest")

    if random_forest_image.exists():
        st.image(
            str(random_forest_image),
            use_container_width=True
        )
    else:
        st.warning("Random Forest image not found.")

st.divider()

# --------------------------------------------------
# 5. SAMPLE PREDICTION
# --------------------------------------------------

st.header("5. Sample Prediction")

st.write(
    "Upload a CSV file containing CAN-BUS feature records. "
    "The trained Decision Tree model will classify the records."
)

uploaded_file = st.file_uploader(
    "Upload CAN-BUS CSV file",
    type=["csv"]
)

if uploaded_file is not None:

    try:

        input_data = pd.read_csv(uploaded_file)

        missing_columns = [
            column
            for column in FEATURE_COLUMNS
            if column not in input_data.columns
        ]

        if missing_columns:

            st.error(
                "Missing columns: "
                + ", ".join(missing_columns)
            )

        elif input_data.empty:

            st.error("The uploaded CSV file is empty.")

        else:

            input_features = input_data[FEATURE_COLUMNS].copy()

            input_features = input_features.apply(
                pd.to_numeric,
                errors="coerce"
            )

            if input_features.isnull().any().any():

                st.error(
                    "The CSV contains missing or invalid "
                    "feature values."
                )

            else:

                st.subheader("Uploaded Records")

                st.dataframe(
                    input_features.head(10),
                    use_container_width=True
                )

                if st.button("Run Prediction"):

                    if not MODEL_PATH.exists():

                        st.error(
                            "Decision Tree model not found."
                        )

                    else:

                        model = joblib.load(MODEL_PATH)

                        predictions = model.predict(
                            input_features
                        )

                        results = input_features.copy()

                        results["Prediction"] = [
                            "Attack" if value == 1 else "Normal"
                            for value in predictions
                        ]

                        st.subheader("Prediction Results")

                        st.dataframe(
                            results,
                            use_container_width=True
                        )

                        attack_count = int(
                            (predictions == 1).sum()
                        )

                        normal_count = int(
                            (predictions == 0).sum()
                        )

                        col1, col2 = st.columns(2)

                        col1.metric(
                            "Normal Records",
                            normal_count
                        )

                        col2.metric(
                            "Attack Records",
                            attack_count
                        )

    except Exception as error:

        st.error(f"Error processing the CSV file: {error}")

st.divider()

# --------------------------------------------------
# 6. DATASET LIMITATIONS
# --------------------------------------------------

st.header("6. Dataset Limitations")

st.warning(
    "All 587,521 attack records in the current dataset "
    "have the same feature combination. Perfect evaluation "
    "results do not prove detection of previously unseen "
    "attack patterns."
)

st.info(
    "This dashboard is a research prototype. "
    "It performs offline CSV predictions and does not "
    "provide live CAN-BUS monitoring."
)

st.caption(
    "CAN-BUS-IDS | Week 6 - Dashboard Development"
)
