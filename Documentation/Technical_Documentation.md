# Technical Documentation: System Architecture & Execution Guide

**AIORI Hackathon 3 — Problem Statement PS-001 | Team: Cipher Aegis**

---

## 1. Environment & Prerequisites

    The project requires the following verified software environment:

    • **Operating System:** macOS (Apple Silicon / Intel) or Linux (Ubuntu 22.04+)

    • **Java Runtime:** Eclipse Temurin JDK 21 (build 21.0.12.1+1-LTS) or OpenJDK 20+

    • **Android SDK:** Android API 36 / 37, Build-Tools 36.0.0, Platform-Tools v35.0.0+

    • **Android Build Tools:** Gradle 9.6.0 wrapper, Android Gradle Plugin (AGP) 9.5.0

    • **Python Environment:** Python 3.10.13 with NumPy 2.2.6, Scikit-Learn 1.7.2, Pandas 2.3.3, Streamlit 1.54.0, Joblib 1.5.2, Matplotlib 3.10.7, Seaborn 0.13.2, ReportLab 5.1.0, and Python-PPTX 1.0.2.
    

## 2. Repository Layout
```text
A3-PS001-TC372/
    ├── AndroidApp/          # Native Kotlin & Jetpack Compose application
    │   ├── app/src/main/    # MainActivity.kt, SimulationEngine.kt, Theme
    │   ├── app/src/test/    # SimulationEngineTest.kt (Unit Test Suite)
    │   └── build.gradle.kts # AGP 9.5.0, Target SDK 37, Min SDK 24
    ├── ML/
    │   ├── data/raw/        # synthetic_events.csv, android_simulation_events.csv
    │   ├── data/processed/  # features.csv, train.csv, validation.csv, test.csv
    │   ├── models/          # random_forest.pkl, feature_columns.pkl
    │   ├── results/         # metrics.csv, test_predictions.csv, delay results, figures
    │   └── src/             # Data gen, feature extraction, train, evaluate, predict
    ├── Dashboard/           # 10-Page Streamlit Analytical Web Application (app.py)
    ├── Documentation/       # Reports, Technical Guides, Manuals (Markdown + PDF)
    ├── Presentation/        # PowerPoint Deck (20 slides) & Speaking Script
    ├── Video/               # Video Demonstration Script & Visual Storyboard
    └── tests/               # Python end-to-end integration test suite
```

## 3. Module APIs

    **1. feature_extraction.py**

    • <code>extract_window_features(df, window_duration=30.0, slide_interval=10.0)</code>: Chronologically groups events into rolling windows. Auto-populates missing fields, handles empty windows, and avoids lookahead bias.

    

    **2. explainability.py**

    • <code>ExplainableWarningEngine.evaluate_window(features, rf_pred, rf_prob, timestamp)</code>: Generates threat severity ratings (NORMAL, LOW, MEDIUM, HIGH) and synthesizes primary diagnostic justifications.

    

    **3. preprocessing.py**

    • <code>partition_by_scenario(features_df, test_scenarios, val_ratio=0.1765)</code>: Partitions 240 scenarios into 168 Train, 36 Validation, and 36 Test scenarios, ensuring zero overlapping window leakage across splits.

    

    **4. train_model.py & evaluate_model.py**

    • <code>train_early_warning_model()</code>: Fits 200 estimators with balanced class weighting.

    • <code>evaluate_test_set()</code>: Benchmarks RF against fixed-threshold baseline on the 36 test scenarios, computing confusion matrices, detection delay per scenario, and 300 DPI figures.

    

    **5. predict.py**

    • <code>EarlyWarningPredictor.predict_raw_events_csv(path)</code>: Executes end-to-end inference from raw Android event CSV directly to early-warning alerts.
    

## 4. Execution Commands
```bash
# 1. Run Complete Machine Learning Pipeline
    python ML/src/preprocessing.py
    python ML/src/train_model.py
    python ML/src/evaluate_model.py

    # 2. Run End-to-End System Integration Tests
    python tests/test_end_to_end.py

    # 3. Build & Test Android Native Application
    cd AndroidApp
    ./gradlew testDebugUnitTest
    ./gradlew assembleDebug

    # 4. Launch 10-Page Interactive Dashboard
    streamlit run Dashboard/app.py
```
