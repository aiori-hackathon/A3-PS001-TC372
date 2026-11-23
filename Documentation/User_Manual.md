# User & Operator Manual: Android Simulation & Dashboard Guide

**AIORI Hackathon 3 — Problem Statement PS-001 | Team: Cipher Aegis**

---

## Part 1: Operating the Android Lab Simulator

    The Android laboratory application provides safe, sandboxed generation of file-system operations:

    - **Launch the App:** Deploy <code>app-debug.apk</code> to an Android emulator (API 34+) or test device.

    - **Select Simulation Mode:**

      &nbsp;&nbsp;1. *Normal Activity:* Simulates legitimate document editing (40 files, writes + edits, 150ms pacing).

      &nbsp;&nbsp;2. *Moderate Suspicious:* Generates controlled modifications, 10 renames, and 5 deletions.

      &nbsp;&nbsp;3. *High-Intensity Burst:* Generates aggressive multi-file overwriting, 60 extension renames (.locked), and 30 deletions.

    - **Monitor Telemetry:** Observe the real-time activity stream in the 'Simulation' tab.

    - **Inspect Live Diagnostics:** Navigate to the 'Diagnostics' tab to inspect aggregated operation counts and on-device risk assessment pills.

    - **Export Event Log:** Click **Export CSV** to save <code>android_simulation_events.csv</code> via the Storage Access Framework.
    

## Part 2: Operating the Streamlit Web Dashboard

    Start the dashboard using terminal command: <code>streamlit run Dashboard/app.py</code>.

    Use the sidebar radio buttons to navigate between the 10 analytical modules:

    - **Page 1 (Overview):** View system status, executive summary, and headline accuracy metrics.

    - **Page 2 (Dataset Explorer):** Filter and inspect processed rolling windows and Android exported CSV records.

    - **Page 3 (Behavioural Analysis):** Select any scenario to visualize operations over time, velocity, and behavioral ratios.

    - **Page 4 (Detection Centre):** View live alerts, model confidence scores, and granular diagnostic justifications.

    - **Page 5 (Model Performance):** Examine confusion matrices, Gini feature importances, and ROC/PR curves.

    - **Page 6 (Detection Delay Analysis):** Analyze early-warning responsiveness across attack types.

    - **Page 7 (Benign Activity Analysis):** Review zero false-positive validation during photo backup and document editing.

    - **Page 8 (Simulation & Testing):** Run predictions on sample scenarios or **upload your own Android CSV** for instant threat diagnosis.

    - **Page 9 (Reports & Export):** Download CSV summaries of all benchmark metrics and predictions.

    - **Page 10 (About the Project):** Review research objectives, team background, and academic references.
    

## Part 3: Interpreting Alerts

    When the detection engine sounds an alert, it provides three actionable elements:

    1. **Severity Badge:**

       - <font color="#15803d">**NORMAL:**</font> Safe baseline behavior; modification rates within legitimate user thresholds.

       - <font color="#b45309">**MEDIUM RISK:**</font> Elevated modification frequency or minor renaming activity observed.

       - <font color="#b91c1c">**HIGH RISK:**</font> Concurrent rapid extension renaming, in-place overwriting, and batch deletions.

    2. **Primary Diagnostic Reason:** Explains exactly which behavioral metrics exceeded safety thresholds.

    3. **Underlying Feature Counters:** Quantifies total operations, velocity (ops/sec), and unique files affected in the current 30s window.
    
