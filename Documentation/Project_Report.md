# Explainable Early Warning for Android Ransomware-Like Activity Using Rolling-Window Behavioral Analysis

**AIORI Hackathon 3 — Problem Statement PS-001**  
**Team Name:** Cipher Aegis  
**Lead Researcher:** PraisyDeva MahimaiJ (`praisydeva26@karunya.edu.in`)  

---

## Abstract

    Mobile ransomware on the Android platform poses severe threats to personal privacy, organizational assets, and data availability.
    Crypto-ransomware systematically discovers, overwrites, appends malicious extensions to, or deletes user files. Traditional defensive
    paradigms rely upon static signature recognition or post-encryption extortion detection, which routinely fail against zero-day variants,
    dynamic packers, and rapid polymorphic modifications. This research project presents an integrated, controlled-laboratory early-warning
    prototype that detects Android ransomware-like activity using rolling-window behavioral analysis and Machine Learning. The system
    evaluates a continuous stream of file operations extracted across 30-second overlapping time windows evaluated every 10 seconds.
    Ten temporal kinetic features—including operation velocity, in-place modification bursts, extension renaming rates, batch deletion spikes,
    and filesystem spread—are synthesized into an ensemble Random Forest classifier. Evaluated across an independent, unseen test partition of
    36 complete operational scenarios (576 temporal windows, encompassing 289,677 events across the benchmark), the Random Forest model achieves
    an overall classification accuracy of **99.48%**, precision of **100.0%**, recall of **98.32%**, and F1-score of **99.15%**,
    with an optimal **0.0% False Positive Rate**. Crucially, the prototype achieves a median detection delay of **8.5 seconds** (mean 7.94s)
    from attack initiation, reliably sounding an alarm before attack completion. Furthermore, every alert is augmented by an Explainable Early-Warning
    Engine translating model probabilities into human-interpretable severity categories and granular diagnostic justifications.
    

## 1. Introduction & Problem Statement

    Android devices have become primary computing endpoints, holding confidential communications, personal photographs, banking credentials,
    and enterprise data. Consequently, Android crypto-ransomware families (such as Simplocker, DoubleLocker, FileCoder, and Ro毒) represent
    a devastating threat. Traditional defenses face fundamental architectural limitations:
    


    - **Signature Fragility:** Signature-based antivirus engines identify known hashes or static byte sequences. Attackers bypass them trivially using code obfuscation, reflection, native payloads, or dynamic payload staging.<br/>
    - **Lethal Detection Delay:** Heuristic tools often alert users only after ransom notes appear, at which point cryptographic key destruction has already rendered private user data permanently unrecoverable.<br/>
    - **High False Alarms in Bulk Operations:** Legitimate user tasks—such as gallery cloud backups, batch photo filtering, document auto-saves, and offline cache purges—generate massive file operation bursts. Static rule-based systems inevitably trigger intolerable false alarm rates.
    

## 2. Research Objectives & Questions

    This research investigates five fundamental scientific questions:

    **RQ1:** Can temporal behavioral kinetics distinguish ransomware-like operations from legitimate high-frequency user activities?

    **RQ2:** Can rolling-window analysis achieve early detection before a simulated ransomware attack completes its destructive lifecycle?

    **RQ3:** Does a multi-dimensional Random Forest classifier outperform static threshold baselines on identical evaluation partitions?

    **RQ4:** Can explainable diagnostic engines provide actionable, human-interpretable reasons for machine learning alerts?

    **RQ5:** What are the architectural and privacy constraints of implementing behavioral detection within modern Android sandboxing boundaries?
    

## 3. Experimental Results Benchmark

| Metric | Fixed-Threshold Baseline | Proposed Random Forest | Research Significance |
|---|---|---|---|
| Accuracy | 31.08% | 99.48% | +68.40% improvement |
| Precision | 31.08% | 100.00% | Zero false alarms |
| Recall | 100.00% | 98.32% | Missed only 3 boundary windows |
| F1-Score | 0.4742 | 0.9915 | Superior harmonic balance |
| False Positive Rate | 100.00% | 0.00% | Critical for practical usability |
| True Negatives (TN) | 0 | 397 | Correct benign classifications |
| False Positives (FP) | 397 | 0 | Baseline flagged all benign tasks |
| False Negatives (FN) | 0 | 3 | Transient onset windows |
| True Positives (TP) | 179 | 176 | Robust attack detection |


## 4. Detection Delay Analysis

    A critical contribution of this project is measuring **Detection Delay**: the elapsed duration between the adversary's
    first malicious operation (<code>attack_start</code>) and the earliest time window triggering a suspicious alert.

    - **Scenario Detection Rate:** 100.0% (18/18 suspicious attack scenarios detected before termination).

    - **Average Detection Delay:** **7.94 seconds** across all attack patterns.

    - **Median Detection Delay:** **8.50 seconds**.

    - **Fastest Detection:** **2.0 seconds** (rapid rename burst).

    - **Slowest Detection:** **14.0 seconds** (gradual stealthy attack).

    Because all attacks had durations exceeding 80–120 seconds, the 7.94s average delay enables defense interventions before significant data loss occurs.
    

## 5. Architectural Limitations & Ethical Scope

    - **Controlled Laboratory Scope:** Evaluated on synthetic and lab-simulated telemetry within the application's private sandbox (<code>context.filesDir</code>).

    - **Android Sandbox Enforcement:** Android's UID-based process isolation strictly prohibits third-party user apps from observing or intercepting file I/O operations of other applications without root privileges or Device Policy Controller enrollment.

    - **Simulated vs. Real Ransomware:** Simulated ransomware mimics file system kinetics without deploying destructive cryptographic locks or malware propagation payloads.

    - **Future Work:** Evaluating integration with Accessibility telemetry, Android Scoped Storage media providers, and hardware telemetry (e.g. CPU/thermal side-channels).
    

## 6. Conclusion

    This project successfully designed, implemented, and benchmarked an explainable early-warning prototype for Android ransomware-like activity.
    The primary research contributions include: (1) formalizing 10 rolling-window behavioral kinetic features for Android file systems;
    (2) demonstrating that Random Forest eliminates the 100% false-alarm rate of heuristic baselines while achieving 99.48% accuracy;
    (3) proving empirical early-warning capability with an average detection delay of 7.94 seconds; and (4) delivering an integrated,
    fully functional system comprising a native Android lab application, ML training pipeline, and 10-page Streamlit analytical dashboard.
    
