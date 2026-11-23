# Video Demonstration Script: Cipher Aegis (PS-001)

SCENE 1: PROJECT INTRODUCTION (0:00 - 0:35)
    [Visual: Title Slide & Dashboard Overview Page]
    Narration: "Hello everyone. Welcome to the demonstration of Cipher Aegis, our submission for AIORI Hackathon 3, Problem Statement PS-001: Explainable Early Warning for Android Ransomware-Like Activity Using Rolling-Window Behavioral Analysis. In this video, we will walk you through our complete integrated prototype, starting from the native Android laboratory app to our rolling-window feature extraction, Random Forest detection engine, and interactive research dashboard."

    SCENE 2: ANDROID SIMULATOR — NORMAL ACTIVITY (0:35 - 1:15)
    [Visual: Android Emulator / App Screen running 'Normal Activity']
    Narration: "We begin on the Android laboratory application. Notice our clean Material 3 interface. The app operates strictly within its private sandbox directory, context.filesDir, ensuring personal files remain completely untouched. We now click 'Run Normal Activity'. The app creates and edits 40 simulated documents with standard pacing. Looking at the live telemetry stream and diagnostics tab, the system records 80 events and classifies the state as 'NORMAL - Benign Legitimate Activity'."

    SCENE 3: ANDROID SIMULATOR — MODERATE & HIGH BURST (1:15 - 2:05)
    [Visual: Android App running 'Moderate' then 'High-Intensity Burst']
    Narration: "Next, we run 'Moderate Suspicious Activity'. The app introduces rapid file modifications, 10 file extension renames, and 5 deletions. The diagnostics card immediately elevates to 'MEDIUM RISK'. Now, we trigger 'High-Intensity Ransomware Burst'. Watch the telemetry: 60 files undergo aggressive multi-pass overwrites, followed by 60 extension renames to dot-locked, and 30 deletions. The diagnostics engine instantly signals 'HIGH RISK - Ransomware-Like Activity Burst Detected'. We click 'Export CSV' to save our telemetry log."

    SCENE 4: STREAMLIT DASHBOARD — BEHAVIORAL & DETECTION CENTRES (2:05 - 3:00)
    [Visual: Streamlit Dashboard Pages 3 & 4]
    Narration: "Moving over to our Streamlit dashboard, on Page 3, Behavioral Analysis, we select the scenario we just exported. We can visualize the operation velocity spike exceeding 15 operations per second and the sudden leap in the rename ratio. On Page 4, Detection Centre, our trained Random Forest model evaluates the stream in 30-second rolling windows. For every suspicious window, our Explainable Early-Warning Engine generates a diagnostic card detailing the exact reason, threat confidence, and affected file metrics."

    SCENE 5: MODEL PERFORMANCE & DETECTION DELAY (3:00 - 3:45)
    [Visual: Streamlit Dashboard Pages 5 & 6]
    Narration: "On Page 5, Model Performance, we review our verified benchmarks across 36 unseen scenarios. The Random Forest achieves 99.48% accuracy with a 0% false positive rate. Comparing this to the fixed-threshold baseline on the left, the baseline triggers false alarms on 100% of benign tasks, whereas Random Forest handles photo backups and document editing flawlessly. On Page 6, our detection delay analysis shows an average alert time of just 7.94 seconds from attack onset."

    SCENE 6: LIVE CSV UPLOAD & CONCLUSION (3:45 - 4:30)
    [Visual: Page 8 CSV upload demonstration & Page 10 Conclusion]
    Narration: "On Page 8, Simulation and Testing, users can drag and drop any exported Android CSV log. The system extracts rolling windows in real time, executes model inference, and outputs early warnings within milliseconds. To conclude, Cipher Aegis delivers a robust, explainable, and scientifically validated early-warning prototype that safeguards Android devices before ransomware damage is irreversible. Thank you!"