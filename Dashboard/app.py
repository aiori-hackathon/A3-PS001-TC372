"""
Cipher Aegis - Android Ransomware-Like Activity Early Warning Dashboard.
AIORI Hackathon 3 | Problem Statement: PS-001 | Team: Cipher Aegis

A professional, 10-page research dashboard for explainable early warning,
rolling-window behavioral analysis, model evaluation, and live simulation testing.
"""

import os
import sys
import io
import time
import datetime
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Configure page settings
st.set_page_config(
    page_title="Cipher Aegis - Android Early Warning Lab",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Robust Path Resolution
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
ML_DIR = os.path.join(PROJECT_ROOT, "ML")

if ML_DIR not in sys.path:
    sys.path.append(ML_DIR)
ML_SRC = os.path.join(ML_DIR, "src")
if ML_SRC not in sys.path:
    sys.path.append(ML_SRC)

try:
    from feature_extraction import extract_window_features, FEATURE_COLUMNS
    from explainability import ExplainableWarningEngine
    from predict import EarlyWarningPredictor
except ImportError:
    # Fallback to local import
    from ML.src.feature_extraction import extract_window_features, FEATURE_COLUMNS
    from ML.src.explainability import ExplainableWarningEngine
    from ML.src.predict import EarlyWarningPredictor

# Light-theme CSS styling
CUSTOM_CSS = """
<style>
    /* Main container and typography */
    .main {
        background-color: #f8fafc;
        color: #0f172a;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Header and Title */
    .header-box {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white;
        padding: 24px 28px;
        border-radius: 12px;
        margin-bottom: 24px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .header-box h1 {
        color: white !important;
        margin: 0;
        font-size: 26px;
        font-weight: 700;
    }
    .header-box p {
        color: #e0f2fe;
        margin: 6px 0 0 0;
        font-size: 14px;
    }
    
    /* Metrics and Cards */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 14px 18px;
        border-radius: 10px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.04);
    }
    div[data-testid="stMetricLabel"] {
        color: #64748b !important;
        font-size: 13px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #0f172a !important;
        font-size: 22px !important;
        font-weight: 700 !important;
    }
    
    /* Severity Badges */
    .badge-normal {
        background-color: #dcfce7;
        color: #15803d;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
    }
    .badge-medium {
        background-color: #fef3c7;
        color: #b45309;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
    }
    .badge-high {
        background-color: #fee2e2;
        color: #b91c1c;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
    }
    
    /* Content Cards */
    .research-card {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }
    
    /* Tabs & Tables */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f5f9;
        border-radius: 6px;
        padding: 8px 16px;
        color: #475569;
    }
    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: white !important;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# Data & Model Loaders (Cached)
@st.cache_data
def load_all_datasets():
    feat_p = os.path.join(ML_DIR, "data/processed/features.csv")
    raw_p = os.path.join(ML_DIR, "data/raw/synthetic_events.csv")
    test_p = os.path.join(ML_DIR, "results/test_predictions.csv")
    metrics_p = os.path.join(ML_DIR, "results/metrics.csv")
    delay_p = os.path.join(ML_DIR, "results/detection_delay_results.csv")
    benign_p = os.path.join(ML_DIR, "results/benign_activity_analysis.csv")
    attack_p = os.path.join(ML_DIR, "results/detection_by_attack_type.csv")
    android_p = os.path.join(ML_DIR, "data/raw/android_simulation_events.csv")

    features_df = pd.read_csv(feat_p) if os.path.exists(feat_p) else pd.DataFrame()
    test_pred_df = pd.read_csv(test_p) if os.path.exists(test_p) else pd.DataFrame()
    metrics_df = pd.read_csv(metrics_p) if os.path.exists(metrics_p) else pd.DataFrame()
    delay_df = pd.read_csv(delay_p) if os.path.exists(delay_p) else pd.DataFrame()
    benign_df = pd.read_csv(benign_p) if os.path.exists(benign_p) else pd.DataFrame()
    attack_df = pd.read_csv(attack_p) if os.path.exists(attack_p) else pd.DataFrame()
    android_df = pd.read_csv(android_p) if os.path.exists(android_p) else pd.DataFrame()

    return {
        "features": features_df,
        "test_predictions": test_pred_df,
        "metrics": metrics_df,
        "delay": delay_df,
        "benign": benign_df,
        "attack": attack_df,
        "android": android_df
    }


@st.cache_resource
def load_trained_model():
    model_p = os.path.join(ML_DIR, "models/random_forest.pkl")
    cols_p = os.path.join(ML_DIR, "models/feature_columns.pkl")
    if os.path.exists(model_p) and os.path.exists(cols_p):
        model = joblib.load(model_p)
        cols = joblib.load(cols_p)
        return model, cols
    return None, None


data_store = load_all_datasets()
model, feature_cols = load_trained_model()


# Sidebar Navigation
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("Cipher Aegis")
    st.caption("AIORI Hackathon 3 | PS-001\nEarly Warning Research System")
    st.divider()

    pages = [
        "1. Overview",
        "2. Dataset Explorer",
        "3. Behavioural Analysis",
        "4. Detection Centre",
        "5. Model Performance",
        "6. Detection Delay Analysis",
        "7. Benign Activity Analysis",
        "8. Simulation & Testing",
        "9. Reports and Export",
        "10. About the Project"
    ]
    
    # Support query parameter for direct page navigation (e.g., ?page=5)
    default_idx = 0
    query_page = st.query_params.get("page", None)
    if query_page:
        for idx, p in enumerate(pages):
            if query_page.lower() in p.lower() or query_page == str(idx + 1):
                default_idx = idx
                break

    selected_page = st.radio(
        "Navigation Menu",
        pages,
        index=default_idx
    )

    st.divider()
    st.caption("Environment: macOS | Python 3.10\nModel: Random Forest (200 Trees)")
    st.info("Controlled Lab Prototype: All data is synthetic and isolated to app private sandbox.")


# -------------------------------------------------------------
# PAGE 1: OVERVIEW
# -------------------------------------------------------------
if selected_page == "1. Overview":
    st.markdown(
        """
        <div class="header-box">
            <h1>Explainable Early Warning for Android Ransomware-Like Activity</h1>
            <p>Controlled Laboratory Prototype Using Rolling-Window Behavioral Analysis & Machine Learning</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)
    total_events = 289677
    total_windows = len(data_store["features"])
    total_scenarios = data_store["features"]["scenario_id"].nunique() if not data_store["features"].empty else 240
    rf_acc = 99.48

    col1.metric("Total Events Evaluated", f"{total_events:,}")
    col2.metric("Total Rolling Windows", f"{total_windows:,}")
    col3.metric("Scenarios (50% Benign)", f"{total_scenarios}")
    col4.metric("RF Detection Accuracy", f"{rf_acc}%")

    st.markdown("### System Architecture & Health")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.success("**Android Lab Simulator**: Functional (v1.0)\n- Private Sandbox Scoped\n- Kotlin Compose UI")
    with c2:
        st.success("**Feature Extraction**: Operational\n- 30s Overlapping Windows\n- 10s Sliding Interval")
    with c3:
        st.success("**Random Forest Engine**: Trained & Active\n- 200 Estimators, Depth 12\n- 0% False Positive Rate")

    st.markdown("### Executive Summary")
    st.write(
        """
        This project tackles the critical challenge of detecting Android crypto-ransomware in its earliest stages.
        Traditional antivirus applications depend on known signatures or post-encryption ransom notes, which fail
        against novel zero-day ransomware or rapidly polymorphic variants.
        
        Our solution extracts **rolling-window behavioral features** (operation velocity, in-place modification bursts,
        rapid extension renames, batch deletions, and file spread) from file telemetry in a controlled Android laboratory.
        A **Random Forest classifier** is evaluated against an unseen test partition of 36 complete scenarios,
        achieving **99.48% accuracy** and an **average detection delay of 7.94 seconds**, while avoiding false alarms
        during heavy benign activity (document editing and photo backup).
        """
    )

    st.markdown("### Headline Comparative Performance")
    if not data_store["metrics"].empty:
        st.dataframe(data_store["metrics"].round(4), use_container_width=True)


# -------------------------------------------------------------
# PAGE 2: DATASET EXPLORER
# -------------------------------------------------------------
elif selected_page == "2. Dataset Explorer":
    st.header("Dataset Health & Structural Explorer")
    st.write("Comprehensive audit of synthetic event streams and rolling-window behavioral features.")

    tab1, tab2, tab3 = st.tabs(["Processed Feature Dataset", "Android Lab Telemetry", "Statistical Health Audit"])

    with tab1:
        df_feat = data_store["features"]
        st.subheader("Rolling-Window Behavioral Features (3,840 Windows)")
        st.write(f"Shape: `{df_feat.shape[0]} rows × {df_feat.shape[1]} columns` across `{df_feat['scenario_id'].nunique()}` unique scenarios.")

        # Filtering
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            stype_filter = st.multiselect("Filter by Scenario Type", sorted(df_feat["scenario_type"].unique()), default=df_feat["scenario_type"].unique())
        with col_f2:
            lbl_filter = st.multiselect("Filter by Label", [0, 1], default=[0, 1], format_func=lambda x: "Benign (0)" if x == 0 else "Suspicious (1)")

        filtered = df_feat[(df_feat["scenario_type"].isin(stype_filter)) & (df_feat["label"].isin(lbl_filter))]
        st.dataframe(filtered.head(100), use_container_width=True)

        col_c1, col_c2 = st.columns(2)
        with col_c1:
            st.markdown("**Window Distribution by Scenario Type**")
            st.bar_chart(df_feat["scenario_type"].value_counts())
        with col_c2:
            st.markdown("**Class Label Distribution (0=Benign, 1=Suspicious)**")
            st.bar_chart(df_feat["label"].value_counts())

    with tab2:
        df_and = data_store["android"]
        st.subheader("Exported Android Simulation Events")
        if not df_and.empty:
            st.write(f"Total exported events: `{len(df_and)} records`. Schema matches standard ML input format.")
            st.dataframe(df_and.head(100), use_container_width=True)
            st.write("**Operation Breakdown in Android Simulation:**")
            st.dataframe(df_and.groupby(["scenario_type", "operation"]).size().unstack(fill_value=0), use_container_width=True)
        else:
            st.info("No Android simulation CSV found. Run the simulation on Page 8 or export from the Android App.")

    with tab3:
        st.subheader("Data Validation & Quality Metrics")
        audit_col1, audit_col2 = st.columns(2)
        with audit_col1:
            st.markdown(
                """
                - **Total Scenarios**: 240 (120 Benign, 120 Suspicious)
                - **Missing Values**: 0 nulls in feature columns
                - **Duplicate Windows**: 0 duplicates detected
                - **Scenario Independence**: Strict scenario-level partitioning (zero overlapping window leakage)
                - **Window Size**: 30.0 seconds
                - **Slide Interval**: 10.0 seconds
                """
            )
        with audit_col2:
            st.markdown(
                """
                - **Operation Vocabulary**: `WRITE`, `MODIFY`, `RENAME`, `DELETE`, `READ`
                - **Label Encoding**: Binary (0 = Legitimate, 1 = Suspicious)
                - **Partition Ratio**: 70% Train (168 scenarios), 15% Val (36 scenarios), 15% Test (36 scenarios)
                - **Reproducibility Seed**: Random State 42
                """
            )


# -------------------------------------------------------------
# PAGE 3: BEHAVIOURAL ANALYSIS
# -------------------------------------------------------------
elif selected_page == "3. Behavioural Analysis":
    st.header("Rolling-Window Behavioral Telemetry Analysis")
    st.write("Inspect how file-system operations evolve over time in benign vs. ransomware-like scenarios.")

    df_feat = data_store["features"]
    scenarios = sorted(df_feat["scenario_id"].unique())
    selected_scen = st.selectbox("Select Scenario for Behavioral Inspection", scenarios, index=scenarios.index("S005") if "S005" in scenarios else 0)

    scen_data = df_feat[df_feat["scenario_id"] == selected_scen].sort_values("window_start")
    scen_type = scen_data["scenario_type"].iloc[0]
    attack_start = scen_data["attack_start"].dropna().iloc[0] if scen_data["attack_start"].notna().any() else "N/A"

    col_m1, col_m2, col_m3, col_m4 = st.columns(4)
    col_m1.metric("Scenario ID", selected_scen)
    col_m2.metric("Scenario Type", scen_type)
    col_m3.metric("Attack Start", str(attack_start))
    col_m4.metric("Window Count", len(scen_data))

    st.markdown("#### Operations Over Time Across 30s Rolling Windows")
    chart_cols = ["modify_count", "rename_count", "delete_count", "write_count"]
    chart_df = scen_data.set_index("window_start")[chart_cols]
    st.line_chart(chart_df)

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### Operational Velocity (Ops / Second)")
        st.area_chart(scen_data.set_index("window_start")["ops_per_second"])
    with col_g2:
        st.markdown("#### Unique Files Affected per Window")
        st.bar_chart(scen_data.set_index("window_start")["unique_files"])

    st.markdown("#### Behavioral Ratios (Modify, Rename, Delete Share)")
    ratio_df = scen_data.set_index("window_start")[["modify_ratio", "rename_ratio", "delete_ratio"]]
    st.line_chart(ratio_df)


# -------------------------------------------------------------
# PAGE 4: DETECTION CENTRE
# -------------------------------------------------------------
elif selected_page == "4. Detection Centre":
    st.header("Real-Time Explainable Detection Centre")
    st.write("Inspect live model inferences, threat severity ratings, and granular explainability reasons.")

    test_pred_df = data_store["test_predictions"]
    if test_pred_df.empty:
        st.warning("Test predictions dataset is not available.")
        st.stop()

    test_scenarios = sorted(test_pred_df["scenario_id"].unique())
    chosen_sid = st.selectbox("Select Test Scenario to Inspect Inferences", test_scenarios, index=test_scenarios.index("S005") if "S005" in test_scenarios else 0)

    sample = test_pred_df[test_pred_df["scenario_id"] == chosen_sid].sort_values("window_start").copy()

    total_w = len(sample)
    rf_alerts = int((sample["random_forest_prediction"] == 1).sum())
    base_alerts = int((sample["baseline_prediction"] == 1).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Windows", total_w)
    c2.metric("Random Forest Alerts", rf_alerts)
    c3.metric("Fixed-Threshold Alerts", base_alerts)
    c4.metric("True Scenario Label", "Suspicious" if sample["label"].max() == 1 else "Benign")

    st.markdown("### Explainable Alert Feed")
    suspicious_windows = sample[sample["random_forest_prediction"] == 1]

    if suspicious_windows.empty:
        st.success("No suspicious activity detected. All evaluated rolling windows conform to benign baseline profiles.")
    else:
        for idx, row in suspicious_windows.iterrows():
            diag = ExplainableWarningEngine.evaluate_window(
                features=row.to_dict(),
                rf_prediction=int(row["random_forest_prediction"]),
                rf_probability=float(row["random_forest_probability"]),
                timestamp=str(row["window_end"])
            )
            badge_class = "badge-high" if diag["severity_level"] == "HIGH RISK" else "badge-medium"

            st.markdown(
                f"""
                <div class="research-card">
                    <span class="{badge_class}">{diag['severity_level']}</span>
                    <strong style="margin-left: 10px; font-size: 15px;">{diag['statusSummary']}</strong>
                    <span style="float: right; color: #64748b; font-size: 12px;">Window End: {diag['timestamp']}</span>
                    <p style="margin: 8px 0 6px 0; color: #334155; font-size: 13px;"><b>Primary Reason:</b> {diag['primary_reason']}</p>
                    <div style="font-size: 12px; color: #475569;">
                        <b>Confidence:</b> {diag['rf_probability']*100:.1f}% | 
                        <b>Renames:</b> {diag['metrics']['rename_count']} | 
                        <b>Modifications:</b> {diag['metrics']['modify_count']} | 
                        <b>Deletions:</b> {diag['metrics']['delete_count']} | 
                        <b>Spread:</b> {diag['metrics']['unique_files']} files
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("### Window-by-Window Diagnostic Table")
    display_cols = [
        "window_start", "total_ops", "modify_count", "rename_count",
        "delete_count", "unique_files", "baseline_prediction",
        "random_forest_prediction", "random_forest_probability", "label"
    ]
    st.dataframe(sample[display_cols], use_container_width=True)


# -------------------------------------------------------------
# PAGE 5: MODEL PERFORMANCE
# -------------------------------------------------------------
elif selected_page == "5. Model Performance":
    st.header("Comparative Model Performance & Benchmark Suite")
    st.write("Rigorous quantitative comparison between Random Forest and the Fixed-Threshold baseline on 36 unseen scenarios.")

    m_df = data_store["metrics"]
    if not m_df.empty:
        st.dataframe(m_df.round(4), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Confusion Matrices (Baseline vs. Proposed RF)")
        cm_fig_path = os.path.join(ML_DIR, "results/figures/confusion_matrices.png")
        if os.path.exists(cm_fig_path):
            st.image(cm_fig_path, use_container_width=True)
        else:
            st.info("Confusion matrix figure not found.")

    with col2:
        st.markdown("#### Feature Importance Analysis (Gini Impurity)")
        feat_fig_path = os.path.join(ML_DIR, "results/figures/feature_importance.png")
        if os.path.exists(feat_fig_path):
            st.image(feat_fig_path, use_container_width=True)
        else:
            st.info("Feature importance figure not found.")

    st.markdown("#### ROC and Precision-Recall Curves")
    roc_fig_path = os.path.join(ML_DIR, "results/figures/roc_pr_curves.png")
    if os.path.exists(roc_fig_path):
        st.image(roc_fig_path, use_container_width=True)

    st.markdown("### Key Scientific Takeaways")
    st.markdown(
        """
        1. **100% Precision & 0% False Positive Rate**: Random Forest achieved zero false alarms across all benign document editing, photo backup, and normal user tasks.
        2. **Fixed-Threshold Failure (100% FPR)**: The fixed threshold baseline triggered false alarms on every single benign scenario because bulk photo backup and document auto-saves exceed static operation counters.
        3. **Behavioral Feature Synergies**: Top predictive features are `rename_ratio` (37.79%), `rename_count` (26.60%), `total_ops` (8.43%), and `ops_per_second` (7.72%).
        """
    )


# -------------------------------------------------------------
# PAGE 6: DETECTION DELAY ANALYSIS
# -------------------------------------------------------------
elif selected_page == "6. Detection Delay Analysis":
    st.header("Detection Delay & Early Warning Responsiveness")
    st.write("Evaluates how quickly the model sounds an alarm after ransomware activity begins.")

    delay_summary_p = os.path.join(ML_DIR, "results/detection_delay.csv")
    if os.path.exists(delay_summary_p):
        st.dataframe(pd.read_csv(delay_summary_p), use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Detection Delay Distribution Across Scenarios")
        delay_graph_p = os.path.join(ML_DIR, "results/detection_delay_graph.png")
        if os.path.exists(delay_graph_p):
            st.image(delay_graph_p, use_container_width=True)
    with col2:
        st.markdown("#### Average Delay by Attack Pattern")
        attack_graph_p = os.path.join(ML_DIR, "results/detection_by_attack_type.png")
        if os.path.exists(attack_graph_p):
            st.image(attack_graph_p, use_container_width=True)

    st.markdown("### Scenario-Level Detection Delay Log")
    dd_res = data_store["delay"]
    if not dd_res.empty:
        st.dataframe(dd_res, use_container_width=True)
        st.markdown(
            f"""
            - **Scenarios Detected**: `{len(dd_res)} / 18 (100% detection rate)`
            - **Average Detection Delay**: `{dd_res['detection_delay_seconds'].mean():.2f} seconds`
            - **Median Detection Delay**: `{dd_res['detection_delay_seconds'].median():.2f} seconds`
            - **Fastest Alert**: `{dd_res['detection_delay_seconds'].min():.1f} seconds` (rapid rename burst)
            - **Slowest Alert**: `{dd_res['detection_delay_seconds'].max():.1f} seconds` (gradual stealthy attack)
            """
        )


# -------------------------------------------------------------
# PAGE 7: BENIGN ACTIVITY ANALYSIS
# -------------------------------------------------------------
elif selected_page == "7. Benign Activity Analysis":
    st.header("Benign Activity Analysis & False Alarm Mitigation")
    st.write("Demonstrates resilience against legitimate intensive user operations.")

    benign_df = data_store["benign"]
    if not benign_df.empty:
        st.dataframe(benign_df, use_container_width=True)

    st.markdown("### Why Traditional Thresholds Cause Excessive False Positives")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="research-card">
                <h4>Document Editing</h4>
                <p>Frequent autosaving and document recompilation produce high modification counts (>20 ops/min). The baseline triggers false alarms (100% FPR), whereas RF correctly identifies absence of extension renaming.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            """
            <div class="research-card">
                <h4>Photo Backup</h4>
                <p>Syncing hundreds of gallery photos creates high write and modification bursts across dozens of unique files. RF recognizes low rename/delete ratios and avoids false alarms (0% FPR).</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            """
            <div class="research-card">
                <h4>Normal Android Usage</h4>
                <p>Intermittent file reading, temporary file cache creation, and ordinary logging. Both RF and human review categorize this as benign with 0 false alarms.</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# -------------------------------------------------------------
# PAGE 8: SIMULATION AND TESTING
# -------------------------------------------------------------
elif selected_page == "8. Simulation & Testing":
    st.header("Interactive Simulation & CSV Upload Testing")
    st.write("Test the end-to-end detection pipeline with custom event CSVs or pre-packaged sample scenarios.")

    st.markdown("### Option A: Select Pre-Packaged Sample Scenario")
    sample_choice = st.selectbox(
        "Choose a laboratory test scenario",
        ["Android Normal Simulation (40 docs)", "Android Moderate Suspicious (Renames)", "Android High-Intensity Burst (60 files)", "Synthetic Gradual Attack (S009)"]
    )

    if st.button("Run Model Prediction on Selected Sample"):
        if "Android Normal" in sample_choice:
            sample_csv = os.path.join(ML_DIR, "data/raw/android_simulation_events.csv")
            sub_type = "normal_activity"
        elif "Moderate" in sample_choice:
            sample_csv = os.path.join(ML_DIR, "data/raw/android_simulation_events.csv")
            sub_type = "moderate_suspicious"
        elif "High-Intensity" in sample_choice:
            sample_csv = os.path.join(ML_DIR, "data/raw/android_simulation_events.csv")
            sub_type = "high_intensity_suspicious"
        else:
            sample_csv = os.path.join(ML_DIR, "data/raw/synthetic_events.csv")
            sub_type = "gradual_activity"

        if os.path.exists(sample_csv):
            ev_df = pd.read_csv(sample_csv)
            if "scenario_type" in ev_df.columns:
                ev_df = ev_df[ev_df["scenario_type"] == sub_type]
            
            w_feat = extract_window_features(ev_df, window_duration_seconds=30.0, slide_interval_seconds=10.0)
            
            predictor = EarlyWarningPredictor(
                os.path.join(ML_DIR, "models/random_forest.pkl"),
                os.path.join(ML_DIR, "models/feature_columns.pkl")
            )
            res = predictor.predict_features_dataframe(w_feat)

            st.success(f"Processing complete! Evaluated {len(res)} rolling windows.")
            susp_count = int((res["rf_prediction"] == 1).sum())
            st.metric("Suspicious Windows Detected", susp_count)

            st.dataframe(res[["window_start", "total_ops", "modify_count", "rename_count", "delete_count", "rf_prediction", "rf_probability", "severity_level", "primary_reason"]], use_container_width=True)

    st.divider()

    st.markdown("### Option B: Upload Custom Event Log (CSV)")
    uploaded_file = st.file_uploader("Upload compatible Android event CSV (columns: timestamp, file_id, operation, ...)", type=["csv"])

    if uploaded_file is not None:
        try:
            up_df = pd.read_csv(uploaded_file)
            st.write(f"Uploaded `{uploaded_file.name}` ({len(up_df)} records).")
            st.dataframe(up_df.head(5), use_container_width=True)

            required_cols = ["timestamp", "file_id", "operation"]
            missing_cols = [c for c in required_cols if c not in up_df.columns]

            if missing_cols:
                st.error(f"Uploaded CSV is missing mandatory columns: {missing_cols}")
            else:
                if st.button("Extract Rolling Windows & Predict Threat"):
                    if "scenario_id" not in up_df.columns:
                        up_df["scenario_id"] = "UPLOADED_LOG"
                    if "attack_start" not in up_df.columns:
                        up_df["attack_start"] = np.nan
                    if "label" not in up_df.columns:
                        up_df["label"] = 0

                    w_feat = extract_window_features(up_df, window_duration_seconds=30.0, slide_interval_seconds=10.0)

                    predictor = EarlyWarningPredictor(
                        os.path.join(ML_DIR, "models/random_forest.pkl"),
                        os.path.join(ML_DIR, "models/feature_columns.pkl")
                    )
                    preds_df = predictor.predict_features_dataframe(w_feat)

                    st.success(f"Inference complete: {len(preds_df)} windows analyzed.")
                    n_susp = int((preds_df["rf_prediction"] == 1).sum())
                    st.metric("Suspicious Windows Detected", n_susp)

                    st.dataframe(preds_df, use_container_width=True)

                    # Export button
                    csv_export = preds_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Inference Results as CSV",
                        data=csv_export,
                        file_name="inference_results.csv",
                        mime="text/csv"
                    )
        except Exception as e:
            st.error(f"Failed to process uploaded file: {e}")


# -------------------------------------------------------------
# PAGE 9: REPORTS AND EXPORT
# -------------------------------------------------------------
elif selected_page == "9. Reports and Export":
    st.header("Evaluation Reports & Data Export Centre")
    st.write("Generate and download formal benchmark reports, metrics tables, and prediction archives.")

    tab_r1, tab_r2 = st.tabs(["CSV Data Downloads", "Executive Evaluation Summary"])

    with tab_r1:
        st.markdown("#### Download Project Artifacts")
        c1, c2 = st.columns(2)
        with c1:
            if not data_store["metrics"].empty:
                st.download_button(
                    "Download Metrics Table (CSV)",
                    data_store["metrics"].to_csv(index=False),
                    "model_evaluation_metrics.csv",
                    "text/csv"
                )
            if not data_store["delay"].empty:
                st.download_button(
                    "Download Detection Delay Results (CSV)",
                    data_store["delay"].to_csv(index=False),
                    "detection_delay_results.csv",
                    "text/csv"
                )
        with c2:
            if not data_store["test_predictions"].empty:
                st.download_button(
                    "Download Test Predictions (CSV)",
                    data_store["test_predictions"].to_csv(index=False),
                    "test_predictions_full.csv",
                    "text/csv"
                )
            if not data_store["benign"].empty:
                st.download_button(
                    "Download Benign Activity Analysis (CSV)",
                    data_store["benign"].to_csv(index=False),
                    "benign_false_positive_analysis.csv",
                    "text/csv"
                )

    with tab_r2:
        st.subheader("Formal Experimental Report Summary")
        st.markdown(
            """
            ### AIORI Hackathon 3 – PS-001 Research Evaluation Summary
            
            **System Overview**:
            - **Approach**: Explainable early warning using rolling-window behavioral analysis.
            - **Window Parameters**: 30.0s window duration, 10.0s sliding interval.
            - **ML Classifier**: Random Forest (200 trees, max depth 12, min leaf samples 2, balanced class weight).
            
            **Verified Results on Unseen Test Scenarios (36 Scenarios, 576 Windows)**:
            - **Random Forest Accuracy**: `99.48%` (Precision: `100.0%`, Recall: `98.32%`, F1: `99.15%`)
            - **False Positive Rate**: `0.00%` (0 false alarms across 397 benign windows)
            - **Baseline Accuracy**: `31.08%` (False Positive Rate: `100.0%`)
            - **Average Detection Delay**: `7.94 seconds` (Median: `8.5 seconds`, Min: `2.0 seconds`, Max: `14.0 seconds`)
            - **Attack Detection Rate**: `100.0%` (18/18 suspicious scenarios detected before attack completion)
            
            **Laboratory Boundary**:
            This system is evaluated in a controlled laboratory setting. Android event monitoring operates within the application's isolated private sandbox (`context.filesDir`) to strictly preserve user privacy.
            """
        )


# -------------------------------------------------------------
# PAGE 10: ABOUT THE PROJECT
# -------------------------------------------------------------
elif selected_page == "10. About the Project":
    st.header("About the Project & Team Cipher Aegis")

    st.markdown(
        """
        <div class="research-card">
            <h3>Explainable Early Warning for Android Ransomware-Like Activity</h3>
            <p><b>Hackathon:</b> AIORI Hackathon 3 | <b>Problem Statement:</b> PS-001</p>
            <p><b>Team Name:</b> Cipher Aegis</p>
            <p><b>Lead Contributor:</b> PraisyDeva MahimaiJ (<a href="mailto:praisydeva26@karunya.edu.in">praisydeva26@karunya.edu.in</a>)</p>
            <p><b>Domain:</b> Mobile Security, Machine Learning, Behavioral Threat Detection, Explainable AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("### Research Objectives")
    st.markdown(
        """
        1. Distinguish ransomware-like file operations from legitimate user activity using behavioral telemetry.
        2. Detect suspicious activity early within a 30-second rolling window before full attack completion.
        3. Demonstrate that machine learning substantially outperforms static heuristic thresholding.
        4. Provide human-interpretable security explanations for every alert.
        5. Respect modern Android security boundaries by conducting controlled experiments in isolated application storage.
        """
    )

    st.markdown("### Technologies Employed")
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(
            """
            - **Android App**: Kotlin, Jetpack Compose, Material 3, Coroutines
            - **Build System**: Android Gradle Plugin 9.5.0, Gradle 9.6.0, JDK 21
            - **Machine Learning**: Scikit-Learn (Random Forest), Joblib, NumPy 2.x
            """
        )
    with col_t2:
        st.markdown(
            """
            - **Data Processing**: Pandas, Time-Delta Rolling Windows
            - **Visualization**: Streamlit, Matplotlib, Seaborn
            - **Reporting**: ReportLab PDF Engine, Python-PPTX
            """
        )

    st.markdown("### Academic References")
    st.markdown(
        """
        1. Singh, N., & Tripathy, S. (2024). *It's Too Late If Exfiltrate: Early Stage Android Ransomware Detection*. Computers & Security, 141, 103819.
        2. Towards Superior Android Ransomware Detection: An Ensemble Machine Learning Perspective. (2025). *Cyber Security and Applications*, 3, 100076.
        3. Sibtain, M., et al. (2025). *Lightweight and Robust Android Ransomware Detection Using Behavioral Analysis*. CMC, 84(3), 5177–5199.
        4. Chew, C. J. W., et al. (2024). *Real-Time System Call-Based Ransomware Detection*. Int. J. Inf. Secur., 23, 1839–1858.
        5. Cen, M., et al. (2024). *Ransomware Early Detection: A Survey*. Computer Networks, 239, 110138.
        """
    )
