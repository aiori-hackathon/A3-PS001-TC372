# AIORI-3-HACKATHON-PROJECTS
This repository will contain the code and resources for the AIORI-3 hackathon that will be developed during the AIORI-3

# AIORI Hackathon 3 – PS-001

## Explainable Early Warning for Android Ransomware-Like Activity Using Rolling-Window Behavioral Analysis

### 1. Project Overview

This project develops an early-warning prototype for identifying Android ransomware-like activity in a controlled laboratory environment.

Instead of detecting known malware signatures, the proposed system analyzes file-operation behavior and identifies suspicious activity patterns using rolling-window behavioral features and Machine Learning.

The prototype combines an Android application for controlled event generation, a Random Forest detection model, and a Streamlit dashboard for visualization and analysis.

**Important:** This is a controlled laboratory prototype using simulated activity and synthetic datasets. It is not a live Android antivirus application.

### 2. Objectives

- Generate normal and ransomware-like file activity in a controlled Android application.
- Collect and analyze file-operation events.
- Extract behavioral features using rolling time windows.
- Train a Random Forest classifier to identify suspicious activity.
- Compare machine learning detection with a fixed-threshold baseline.
- Provide explainable alerts and visual performance analysis.

### 3. System Components

**Android Application**
- Developed using Kotlin and Jetpack Compose.
- Generates normal, moderate suspicious, and high-intensity suspicious activity.
- Collects file-operation events within the application's private storage.
- Supports exporting activity events as CSV.

**Machine Learning Detection**
- Random Forest classifier.
- Rolling-window behavioral feature extraction.
- Fixed-threshold baseline comparison.
- Scenario-based model evaluation.

**Streamlit Dashboard**
- Displays experimental performance metrics.
- Allows selection of simulated scenarios.
- Visualizes file activity over time.
- Displays suspicious activity alerts and prediction probabilities.

### 4. Machine Learning Features

The behavioral analysis uses features such as:

- Total file operations
- Modification count
- Rename count
- Delete count
- Write count
- Number of unique files
- Operations per second
- Modification ratio
- Rename ratio
- Delete ratio

### 5. Experimental Results

The current synthetic test evaluation produced the following Random Forest results:

| Metric | Result |
|---|---:|
| Accuracy | 99.48% |
| Precision | 100% |
| Recall | 98.32% |
| F1-score | 99.15% |
| False Positive Rate | 0% |

Confusion matrix:

- True Negatives: 397
- False Positives: 0
- False Negatives: 3
- True Positives: 176

The fixed-threshold baseline produced a 100% false-positive rate on this particular test set. This result reflects the selected baseline thresholds and experimental dataset, not all threshold-based detection systems.

These results are from synthetic controlled experiments and should not be interpreted as real-world Android detection performance.

### 6. Repository Structure

```text
A3-PS001-TC372/
│
├── AndroidApp/
│   └── Android application source code
│
├── ML/
│   ├── data/
│   │   ├── raw/
│   │   └── processed/
│   ├── models/
│   └── results/
│
├── Dashboard/
│   └── app.py
│
├── Documentation/
│
├── requirements.txt
└── README.md
```

The repository also retains the original hackathon presentation and proposed project structure.

### 7. Installation and Execution

#### Requirements

- Python 3
- Android Studio
- Android emulator or compatible Android device
- Required Python libraries listed in `requirements.txt`

#### Run the Streamlit Dashboard

Clone the repository:

```bash
git clone https://github.com/aiori-hackathon/A3-PS001-TC372.git
cd A3-PS001-TC372
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the dashboard:

```bash
streamlit run Dashboard/app.py
```

#### Run the Android Application

1. Open Android Studio.
2. Select Open Project.
3. Select the `AndroidApp` folder.
4. Allow Gradle synchronization to complete.
5. Launch the application using an Android emulator.
6. Run the controlled activity simulations and export events as CSV.

### 8. Limitations

- The current experiments use synthetic and simulated activity.
- Android event collection is limited to the application's own private storage.
- The prototype does not monitor other applications or the entire Android filesystem.
- The reported performance requires validation using additional datasets and real-world benign activity.

### 9. Future Enhancements

- Integrate real Android telemetry within permitted Android security boundaries.
- Expand the dataset with additional benign and suspicious scenarios.
- Evaluate additional machine learning models.
- Improve detection of low-intensity and previously unseen behavior.
- Conduct broader false-positive and detection-delay evaluations.

### 10. Conclusion

The project demonstrates a behavioral early-warning approach for Android ransomware-like activity in a controlled laboratory environment. It combines Android-based event generation, rolling-window feature extraction, Random Forest classification, and explainable dashboard visualization.

The main objective is to investigate whether behavioral machine learning can identify suspicious file-operation patterns while reducing false alarms during benign bulk activity.

---

**AIORI Hackathon 3 | Problem Statement PS-001**  
**Project:** Android Ransomware-Like Activity Early Warning  
**Team:** Cipher Aegis
