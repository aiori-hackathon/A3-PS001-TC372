
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(
    page_title="Android Early Warning",
    page_icon="🛡️",
    layout="wide"
)

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE)
ML_BASE = os.path.join(PROJECT_ROOT, "ML")

st.title("Android Ransomware-Like Activity Early Warning")
st.caption(
    "AIORI Hackathon 3 | PS-001 | Controlled Lab Simulation"
)

st.info(
    "This prototype analyzes synthetic, simulated file-activity "
    "events. It is not a live Android antivirus."
)

features_path = os.path.join(
    BASE, "data/processed/features.csv"
)

model_path = os.path.join(
    BASE, "models/random_forest.pkl"
)

columns_path = os.path.join(
    BASE, "models/feature_columns.pkl"
)

metrics_path = os.path.join(
    BASE, "results/metrics.csv"
)

if not os.path.exists(features_path):
    st.error("Feature dataset not found.")
    st.stop()

if not os.path.exists(model_path):
    st.error("Trained model not found.")
    st.stop()

df = pd.read_csv(features_path)
model = joblib.load(model_path)
feature_columns = joblib.load(columns_path)

# Metrics section
st.header("Experimental Performance")

if os.path.exists(metrics_path):

    metrics = pd.read_csv(metrics_path)

    st.dataframe(
        metrics.round(4),
        use_container_width=True
    )

else:
    st.warning("Evaluation metrics are not available yet.")

st.divider()

# Scenario selection
st.header("Scenario Analysis")

scenario_ids = sorted(df["scenario_id"].unique())

selected_scenario = st.selectbox(
    "Select a simulated scenario",
    scenario_ids
)

sample = df[
    df["scenario_id"] == selected_scenario
].copy()

sample = sample.sort_values("window_start")

# Predictions
sample["rf_prediction"] = model.predict(
    sample[feature_columns]
)

sample["rf_probability"] = model.predict_proba(
    sample[feature_columns]
)[:, 1]

# Baseline
def baseline(row):

    score = 0

    if row["modify_count"] > 15:
        score += 2

    if row["rename_count"] > 8:
        score += 2

    if row["delete_count"] > 8:
        score += 2

    if row["unique_files"] > 20:
        score += 2

    return int(score >= 2)

sample["baseline_prediction"] = sample.apply(
    baseline,
    axis=1
)

# Summary
col1, col2, col3 = st.columns(3)

col1.metric(
    "Total windows",
    len(sample)
)

col2.metric(
    "Random Forest alerts",
    int(sample["rf_prediction"].sum())
)

col3.metric(
    "Baseline alerts",
    int(sample["baseline_prediction"].sum())
)

# Activity chart
st.subheader("File Activity Over Time")

chart_data = sample.set_index("window_start")[
    [
        "total_ops",
        "modify_count",
        "rename_count",
        "delete_count"
    ]
]

st.line_chart(chart_data)

# Alert details
st.subheader("Explainable Alerts")

alerts = sample[
    sample["rf_prediction"] == 1
].copy()

if alerts.empty:

    st.success("No suspicious windows detected.")

else:

    for _, row in alerts.iterrows():

        reasons = []

        if row["modify_count"] > 0:
            reasons.append(
                f"Modifications: {int(row['modify_count'])}"
            )

        if row["rename_count"] > 0:
            reasons.append(
                f"Renames: {int(row['rename_count'])}"
            )

        if row["delete_count"] > 0:
            reasons.append(
                f"Deletions: {int(row['delete_count'])}"
            )

        st.warning(
            "Suspicious activity detected | "
            + " | ".join(reasons)
        )

        st.write(
            "Suspicious probability:",
            round(float(row["rf_probability"]), 3)
        )

# Full table
st.subheader("Window-Level Predictions")

st.dataframe(
    sample[
        [
            "window_start",
            "total_ops",
            "modify_count",
            "rename_count",
            "delete_count",
            "baseline_prediction",
            "rf_prediction",
            "rf_probability",
            "label"
        ]
    ],
    use_container_width=True
)

st.caption(
    "Predictions are experimental outputs from synthetic test data."
)
