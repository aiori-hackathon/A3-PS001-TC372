# Explainable Early Warning for Android Ransomware-Like Activity Using Rolling-Window Behavioral Analysis

[![AIORI Hackathon 3](https://img.shields.io/badge/AIORI%20Hackathon-3%20(PS--001)-0284c7.svg)](https://github.com/aiori-hackathon/A3-PS001-TC372)
[![Team](https://img.shields.io/badge/Team-Cipher%20Aegis-0369a1.svg)](#team)
[![Platform](https://img.shields.io/badge/Platform-Android%20%7C%20Python-10b981.svg)](#system-architecture)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Build-Passing%20(100%25%20Verified)-success.svg)](#software-quality--testing)

---

## Executive Overview

**Cipher Aegis** is an integrated cybersecurity research prototype designed to detect mobile crypto-ransomware in its earliest temporal stages. Developed for **AIORI Hackathon 3 (Problem Statement PS-001)**, the system evaluates continuous file-system telemetry within a controlled Android laboratory setting.

Rather than relying on brittle byte signatures or waiting for destructive ransom notes to appear, the prototype applies **rolling-window temporal analysis** (30-second overlapping windows with 10-second slide intervals) to measure kinetic behavioral characteristics. A balanced **Random Forest classifier** evaluates operational velocity, in-place modification bursts, extension renaming rates, batch deletions, and filesystem spread.

### Key Research Findings

| Evaluation Metric | Fixed-Threshold Baseline | Proposed Random Forest | Research Advantage |
|:---|:---:|:---:|:---|
| **Overall Accuracy** | 31.08% | **99.48%** | **+68.40%** classification improvement |
| **Precision** | 31.08% | **100.00%** | Zero false alarms across benign tasks |
| **Recall (Sensitivity)** | 100.00% | **98.32%** | High sensitivity with early warning |
| **F1-Score** | 0.4742 | **0.9915** | Superior harmonic balance |
| **False Positive Rate (FPR)** | 100.00% | **0.00%** | Solves alert fatigue in mobile security |
| **Average Detection Delay** | 4.50 s | **7.94 s** | Alerts within seconds of attack onset |
| **Attack Detection Rate** | 100.0% | **100.0%** | 18/18 unseen attack scenarios stopped |

> **Ethical & Controlled Scope Disclosure:** This prototype operates strictly within the application's isolated private sandbox directory (`context.filesDir/lab_files`). It simulates ransomware-like kinetic patterns without deploying destructive encryption or performing unauthorized device surveillance.

---

## System Architecture

```text
+-----------------------------------------------------------------------------------+
|                            CIPHER AEGIS PIPELINE                                  |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Android Native Application] (Kotlin + Jetpack Compose)                          |
|    |-- Lab Simulation Engine: Normal | Moderate Suspicious | High-Intensity Burst |
|    |-- Isolated Sandbox Storage: context.filesDir/lab_files/<timestamp>/           |
|    |-- Live Diagnostics: On-device event counting & explainability rules           |
|    +-- Telemetry Exporter (Storage Access Framework)                              |
|           |                                                                       |
|           v (CSV Stream: timestamp, file_id, operation, file_size, label)         |
|                                                                                   |
|  [Preprocessing & Temporal Feature Extraction]                                    |
|    |-- Data Health Audit: Null-checks, duplicate detection, schema validation     |
|    |-- 30s Overlapping Rolling Windows (10s slide interval)                       |
|    |-- Scenario-Level Segregation (Strict zero-data-leakage guarantee)             |
|    +-- 10 Kinetic Features: total_ops, modify_count, rename_count, delete_count,  |
|                             write_count, unique_files, ops_per_sec, ratios        |
|           |                                                                       |
|           v (Normalized Feature Vectors)                                          |
|                                                                                   |
|  [Machine Learning & Explainable Early-Warning Engine]                            |
|    |-- Random Forest Classifier (200 Trees, Depth 12, Balanced Class Weights)     |
|    |-- Threat Severity Categorization: NORMAL | LOW RISK | MEDIUM RISK | HIGH RISK|
|    +-- Explainability Diagnostic Card (Primary reason, indicators, confidence)    |
|           |                                                                       |
|           v                                                                       |
|                                                                                   |
|  [Interactive Streamlit Research Dashboard] (10 Pages)                            |
|    |-- Overview | Dataset Explorer | Behavioral Analysis | Detection Centre       |
|    |-- Model Performance | Detection Delay | Benign Activity | Live Simulation    |
|    +-- Reports & Export Centre | About & Academic Specifications                  |
+-----------------------------------------------------------------------------------+
```

---

## Repository Structure

```text
A3-PS001-TC372/
│
├── AndroidApp/                          # Native Android Laboratory Application
│   ├── app/
│   │   ├── src/main/java/com/aiori/ransomwarewarning/
│   │   │   ├── MainActivity.kt          # Material 3 UI with 3-tab navigation
│   │   │   ├── SimulationEngine.kt      # Safe lab simulation & diagnostic rules
│   │   │   └── ui/theme/                # Light-themed Compose typography & colors
│   │   ├── src/test/java/com/aiori/ransomwarewarning/
│   │   │   └── SimulationEngineTest.kt  # Android unit test suite (100% pass)
│   │   ├── build.gradle.kts             # AGP 9.5.0, target SDK 37, min SDK 24
│   │   └── build/outputs/apk/debug/     # Compiled app-debug.apk (11.7 MB)
│   ├── gradle/wrapper/                  # Gradle 9.6.0 wrapper configuration
│   └── build.gradle.kts                 # Root Gradle build script
│
├── ML/                                  # Machine Learning Engineering Suite
│   ├── data/
│   │   ├── raw/
│   │   │   ├── synthetic_events.csv     # 289,677 event records across 240 scenarios
│   │   │   └── android_simulation_events.csv # 445 exported Android lab events
│   │   └── processed/
│   │       ├── features.csv             # 3,840 rolling windows across 240 scenarios
│   │       ├── train.csv                # 167 training scenarios (2,672 windows)
│   │       ├── validation.csv           # 37 validation scenarios (592 windows)
│   │       └── test.csv                 # 36 unseen test scenarios (576 windows)
│   ├── models/
│   │   ├── random_forest.pkl            # Trained Random Forest model (200 trees)
│   │   └── feature_columns.pkl          # 10 behavioral feature names
│   ├── results/
│   │   ├── metrics.csv                  # Verified RF vs. Baseline comparative table
│   │   ├── test_predictions.csv         # Full 576-window predictions & probabilities
│   │   ├── detection_delay.csv          # Detection delay summary metrics
│   │   ├── detection_delay_results.csv  # Scenario-by-scenario detection delay log
│   │   ├── detection_by_attack_type.csv # Delay breakdown across attack patterns
│   │   ├── benign_activity_analysis.csv # False positive analysis on benign tasks
│   │   └── figures/                     # 300 DPI publication plots
│   │       ├── confusion_matrices.png   # Baseline vs. RF confusion matrices
│   │       ├── feature_importance.png   # Gini impurity feature ranking chart
│   │       ├── detection_delay_graph.png# Detection delay boxplots
│   │       └── roc_pr_curves.png        # ROC and Precision-Recall curves
│   └── src/                             # Python ML Modules
│       ├── data_generation.py           # Reproducible synthetic event generator
│       ├── feature_extraction.py        # 30s rolling-window feature extractor
│       ├── preprocessing.py             # Schema auditing & scenario-level splits
│       ├── train_model.py               # Random Forest training routine
│       ├── evaluate_model.py            # Benchmark evaluation & figure generator
│       ├── predict.py                   # CLI & API inference interface
│       └── explainability.py            # Explainable Early-Warning Engine
│
├── Dashboard/                           # Streamlit Web Application
│   └── app.py                           # Complete 10-page research dashboard
│
├── Documentation/                       # Academic & Technical Deliverables
│   ├── Project_Report.pdf & .md         # 28-section comprehensive academic report
│   ├── Technical_Documentation.pdf & .md# Architecture, module APIs, and setup guide
│   ├── User_Manual.pdf & .md            # Operator manual for Android & Dashboard
│   ├── Testing_Report.pdf & .md         # QA report with 15 test cases (100% pass)
│   ├── Research_Reproducibility.pdf & .md # Seed, parameter, and formula protocol
│   └── generate_all_documentation.py    # ReportLab document compilation script
│
├── Presentation/                        # Presentation Deliverables
│   ├── Project_Presentation.pptx        # 20-slide presentation deck
│   ├── Presentation_Script.docx & .md   # Team presentation speaking script
│   └── generate_presentation_and_video.py # Slide and script generation script
│
├── Video/                               # Video Demonstration Deliverables
│   ├── Video_Script.docx & .md          # Scene-by-scene demonstration script
│   ├── Storyboard.pdf & .md             # Visual storyboard with timecode cues
│   └── youtube_link.txt                 # Team demonstration video link
│
├── tests/                               # System Integration Tests
│   └── test_end_to_end.py               # End-to-end Python pipeline integration test
│
├── app.py                               # Root entrypoint redirecting to Dashboard
├── requirements.txt                     # Pinned Python package dependencies
├── LICENSE                              # Apache 2.0 Open Source License
└── .gitignore                           # Excludes build caches, venvs, and secrets
```

---

## Installation & Quickstart

### 1. Prerequisites
- **Python**: 3.10+ (Recommended: Python 3.10.13 with NumPy 2.x)
- **Java**: JDK 21 (Temurin or OpenJDK)
- **Android SDK**: Platform 36/37, Build-Tools 36.0.0+

### 2. Environment Setup
```bash
# Clone the repository
git clone https://github.com/aiori-hackathon/A3-PS001-TC372.git
cd A3-PS001-TC372

# Install Python dependencies
pip install -r requirements.txt
```

### 3. Launch the Streamlit Dashboard (10 Pages)
```bash
streamlit run Dashboard/app.py
```
*Alternatively, run from root:* `streamlit run app.py`. Access at `http://localhost:8501`.

### 4. Run Machine Learning Pipeline & Tests
```bash
# Verify scenario-level partitions (no leakage)
python ML/src/preprocessing.py

# Train Random Forest model
python ML/src/train_model.py

# Evaluate test set and generate 300 DPI figures
python ML/src/evaluate_model.py

# Run end-to-end system integration tests
python tests/test_end_to_end.py
```

### 5. Build & Test Android Laboratory App
```bash
cd AndroidApp

# Run unit tests
./gradlew testDebugUnitTest

# Build debug APK
./gradlew assembleDebug
# Generated APK: AndroidApp/app/build/outputs/apk/debug/app-debug.apk
```

---

## Experimental Benchmark Details

### 1. Dataset Taxonomy (240 Scenarios, 289k Events)
- **Benign Scenarios (120 total)**:
  - `normal` (40): General user navigation, temporary cache creation.
  - `document_editing` (45): Frequent in-place saves and word processor auto-saves.
  - `photo_backup` (35): High-frequency batch writing across dozens of files.
- **Suspicious Scenarios (120 total)**:
  - `modification_burst` (31): In-place file tampering and high-frequency overwriting.
  - `rename_burst` (46): Rapid extension appending (`.locked`, `.crypto`, `.enc`).
  - `gradual_activity` (43): Slower, stealthy encryption with mixed operations.

### 2. Feature Gini Importances
The trained Random Forest model revealed that file extension renaming kinetics are the single strongest predictors of Android crypto-ransomware:
1. `rename_ratio`: **37.79%** (Primary discriminator for extension modification)
2. `rename_count`: **26.60%** (Volume of renames in 30s window)
3. `total_ops`: **8.43%** (Gross operational throughput)
4. `ops_per_second`: **7.72%** (Temporal operational velocity)
5. `write_count`: **5.76%** (Separates photo backups from overwrites)
6. `modify_count`: **4.58%** (In-place overwrite frequency)
7. `unique_files`: **3.68%** (Filesystem breadth across handles)
8. `modify_ratio`: **3.00%** (Share of window dedicated to modifications)
9. `delete_count`: **1.49%** (Batch deletion / wiper activity)
10. `delete_ratio`: **0.94%** (Proportion of operations deleting files)

### 3. Detection Delay Breakdown Across Attack Patterns
- **Rename Burst**: Mean delay **7.25 s** | Median **8.0 s** | Range: **2.0s – 9.0s**
- **Modification Burst**: Mean delay **8.50 s** | Median **10.0 s** | Range: **3.0s – 11.0s**
- **Gradual Activity**: Mean delay **8.50 s** | Median **8.5 s** | Range: **4.0s – 14.0s**
- **Overall**: Mean delay **7.94 seconds** with **100% detection rate** before scenario completion.

---

## Explainable Early-Warning Engine

Rather than emitting an opaque binary label, every alert provides human-interpretable security intelligence:
- **Risk Severity Levels**: `NORMAL`, `LOW RISK`, `MEDIUM RISK`, `HIGH RISK`.
- **Primary Diagnostic Reason**: Synthesized from measured behavioral anomalies (e.g. *"Rapid file renaming burst (14 renames, 28% of ops); Wide filesystem spread (18 files)"*).
- **Quantifiable Telemetry**: Exact counts of renames, modifications, deletions, velocity, and affected unique files per 30-second window.

---

## Software Quality & Testing

All major system components have been independently and collectively validated:
- **Android Unit Tests**: `SimulationEngineTest.kt` passes 100% of test cases verifying event schema, statistics tracking, CSV export, and safe sandbox isolation.
- **Python Integration Tests**: `tests/test_end_to_end.py` passes 100% of tests verifying Android CSV ingestion, window extraction, RF prediction, and explainability cards.
- **Build Verification**: Gradle 9.6.0 successfully assembles `app-debug.apk` without compilation errors.
- **Dashboard Integrity**: All 10 Streamlit pages execute with zero syntax errors, broken links, or placeholder components.

---

## Team & Contributors

**Team Name:** Cipher Aegis  
**Lead Researcher & Developer:** PraisyDeva MahimaiJ (`praisydeva26@karunya.edu.in`)  
**Institution:** Karunya Institute of Technology and Sciences  
**Hackathon:** AIORI Hackathon 3 (Problem Statement PS-001)  

---

## References

1. Singh, N., & Tripathy, S. (2024). *It's Too Late If Exfiltrate: Early Stage Android Ransomware Detection*. Computers & Security, 141, Article 103819.
2. *Towards Superior Android Ransomware Detection: An Ensemble Machine Learning Perspective*. (2025). Cyber Security and Applications, 3, Article 100076.
3. Sibtain, M., et al. (2025). *Lightweight and Robust Android Ransomware Detection Using Behavioral Analysis and Feature Reduction*. Computers, Materials & Continua, 84(3), 5177–5199.
4. Chew, C. J. W., et al. (2024). *Real-Time System Call-Based Ransomware Detection*. International Journal of Information Security, 23, 1839–1858.
5. Cen, M., et al. (2024). *Ransomware Early Detection: A Survey*. Computer Networks, 239, Article 110138.
6. MITRE Corporation. *Data Encrypted for Impact: ATT&CK Technique T1486*.
7. Android Open Source Project. *Application Sandbox Architecture & Scoped Storage Security Guidelines*.
