# Presentation Speaking Script: Team Cipher Aegis (PS-001)

Slide 1 (Title):
    "Good morning esteemed judges and fellow researchers. Today, our team, Cipher Aegis, is proud to present our project: 'Explainable Early Warning for Android Ransomware-Like Activity Using Rolling-Window Behavioral Analysis'. Mobile ransomware represents one of the most destructive threats in modern cybersecurity, and we are excited to walk you through our controlled laboratory detection architecture."

    Slide 2 & 3 (Problem & The Early Warning Imperative):
    "Android devices store our most confidential personal and enterprise data. When crypto-ransomware strikes, it rapidly encrypts and destroys user files. Traditional signature-based antivirus solutions fail because attackers trivially obfuscate code and alter byte signatures. More importantly, waiting for a ransom note is lethal: by the time an alert sounds, cryptographic keys are gone, and user files are permanently unrecoverable. Our core objective is early warning: identifying ransomware-like file kinetics in the first few seconds of activity."

    Slide 4 & 5 (Literature & Research Objectives):
    "Recent literature in Computers & Security by Singh and Tripathy in 2024, as well as Cen's comprehensive survey, emphasized that file modification velocity and extension renaming are the strongest behavioral indicators. However, static thresholding causes massive false alarms during bulk tasks like photo backup. We set out to answer five key research questions, focusing on whether rolling-window temporal kinetics and Random Forest machine learning can achieve near-zero false alarms while detecting attacks within seconds."

    Slide 6 & 7 (Methodology & System Architecture):
    "Our prototype connects three tightly integrated components: First, a native Android laboratory app developed in Kotlin and Jetpack Compose that safely executes file operations within its private sandbox. Second, a Python rolling-window feature extraction pipeline that analyzes 30-second sliding windows every 10 seconds without future data leakage. Third, an ensemble Random Forest model coupled with an Explainable Warning Engine and an interactive Streamlit dashboard."

    Slide 8 & 9 (Android Application & Dataset Generation):
    "In the Android app, we provide three controlled laboratory simulation levels: Normal activity, Moderate suspicious with file renames, and High-intensity burst with rapid overwriting, locked extension renaming, and deletions. The event streams are exported via the Storage Access Framework. Our full benchmark dataset comprises 289,677 events across 240 scenarios—120 benign and 120 suspicious—incorporating realistic attack start offsets."

    Slide 10 & 11 (Features & Random Forest Model):
    "From each 30-second window, we extract ten kinetic features: operation velocity, modification frequency and ratio, extension rename frequency and ratio, deletion counts, and unique file spread. Our Random Forest classifier utilizes 200 trees with balanced class weighting. Inference executes in under 2 milliseconds, making it exceptionally lightweight."

    Slide 12 & 13 (Leakage Prevention & Explainability):
    "To ensure scientific integrity, we implemented strict scenario-level partitioning: overlapping windows from the same scenario are never split across train and test sets. Furthermore, our Explainable Early-Warning Engine translates model probabilities into four human-interpretable severity categories—Normal, Low Risk, Medium Risk, and High Risk—accompanied by concrete behavioral reasons."

    Slide 14 & 15 (Experimental Benchmarks & Baseline Comparison):
    "When evaluated on an unseen held-out test partition of 36 complete scenarios across 576 rolling windows, the Random Forest model achieved 99.48% accuracy, 100% precision, 98.32% recall, and an optimal 0.0% False Positive Rate across 397 benign windows. In contrast, the fixed-threshold baseline suffered a disastrous 100% false-alarm rate because legitimate activities like photo backups naturally exceed static file counters."

    Slide 16 & 17 (Detection Delay & Benign Resilience):
    "Crucially, our system detected 100% of the attack scenarios with an average detection delay of just 7.94 seconds—and as fast as 2.0 seconds for aggressive bursts. Across all evaluated benign workflows—document editing, photo backup, and normal navigation—our model triggered zero false alarms."

    Slide 18, 19 & 20 (Dashboard, Limitations & Conclusion):
    "Finally, our 10-page Streamlit dashboard provides deep interactive analytics, scenario replays, and a live CSV upload interface. We strictly disclose that our experiments operated within the app's private sandbox, as modern Android OS architecture enforces per-app UID isolation. In conclusion, Cipher Aegis has delivered a complete, validated, explainable early-warning system that eliminates false alarms and detects ransomware attacks within seconds. Thank you, and we welcome your questions!"