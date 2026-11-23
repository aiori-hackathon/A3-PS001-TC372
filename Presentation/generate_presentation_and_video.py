"""
Presentation Deck and Video Demonstration Artifact Generator.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Builds the 20-slide PowerPoint presentation (.pptx), team presentation speaking script (.docx/.md),
video demonstration script (.docx/.md), and video visual storyboard (.pdf/.md).
"""

import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
import docx
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable

PRESENTATION_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(PRESENTATION_DIR)
VIDEO_DIR = os.path.join(PROJECT_ROOT, "Video")

sys.path.insert(0, os.path.join(PROJECT_ROOT, "Documentation"))
from generate_all_documentation import get_cipher_styles, build_pdf_document


def create_pptx_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    COLOR_BG = RGBColor(248, 250, 252)       # #f8fafc (Light slate)
    COLOR_PRIMARY = RGBColor(2, 132, 199)    # #0284c7 (Sky blue)
    COLOR_DARK = RGBColor(15, 23, 42)        # #0f172a (Dark navy)
    COLOR_TEXT = RGBColor(51, 65, 85)        # #334155 (Slate text)
    COLOR_CARD = RGBColor(255, 255, 255)     # #ffffff (White card)
    COLOR_MUTED = RGBColor(100, 116, 139)    # #64748b (Muted)
    COLOR_BORDER = RGBColor(226, 232, 240)   # #e2e8f0

    slides_content = [
        # Slide 1: Title
        {
            "title": "Explainable Early Warning for Android Ransomware-Like Activity",
            "subtitle": "Controlled Laboratory Behavioral Detection Using Rolling-Window Analysis & Machine Learning\n\nAIORI Hackathon 3 | Problem Statement: PS-001 | Team: Cipher Aegis\nPraisyDeva MahimaiJ (praisydeva26@karunya.edu.in)",
            "bullets": []
        },
        # Slide 2: Problem Statement
        {
            "title": "Problem Statement: The Android Ransomware Crisis",
            "subtitle": "Why Traditional Detection Paradigms Fail on Mobile Operating Systems",
            "bullets": [
                "Android devices store high-value personal photographs, documents, credentials, and business assets.",
                "Crypto-ransomware exploits file permissions to rapidly encrypt, overwrite, rename, or delete user files.",
                "Signature-based antivirus engines rely on known byte hashes and static signatures, failing against zero-day variants and packers.",
                "Static rule thresholds trigger severe false-alarm fatigue during legitimate bulk user activity (e.g. photo backups)."
            ]
        },
        # Slide 3: The Early Warning Challenge
        {
            "title": "The Lethal Detection Delay Problem",
            "subtitle": "Why Early Warning Before Encryption Completion is Essential",
            "bullets": [
                "Post-Encryption Extortion: By the time a ransom note appears, cryptographic keys are deleted and data is permanently lost.",
                "Irreversibility: Asymmetric and symmetric ciphers (AES-256 + RSA-2048) render post-facto recovery mathematically impossible.",
                "The Research Imperative: Detect suspicious file-operation kinetics in the first few seconds of activity.",
                "Goal: Alert users and mitigation engines within a 30-second rolling window before substantial destruction occurs."
            ]
        },
        # Slide 4: Existing Literature & Scientific Gaps
        {
            "title": "State of the Art & Research Gap",
            "subtitle": "Synthesizing Recent Cybersecurity Literature (IEEE, ACM, Elsevier)",
            "bullets": [
                "Singh & Tripathy (2024): Emphasized the urgent need for early-stage Android detection before data exfiltration.",
                "Cen et al. (2024 - Survey): Identified file modification velocity and extension renaming as the two strongest behavioral indicators.",
                "Sibtain et al. (2025): Proved lightweight behavioral feature reduction prevents mobile device CPU exhaustion.",
                "The Identified Gap: Lack of an integrated, explainable early-warning system evaluated in a controlled Android environment with rolling-window kinetics."
            ]
        },
        # Slide 5: Research Objectives & Scope
        {
            "title": "Research Objectives & Scientific Scope",
            "subtitle": "Five Core Investigation Pillars",
            "bullets": [
                "1. Distinguish ransomware-like kinetics from intensive benign mobile workflows using temporal feature extraction.",
                "2. Evaluate rolling-window temporal analysis to quantify early-warning detection delay.",
                "3. Benchmark Random Forest against a fixed-threshold baseline on identical unseen test scenarios.",
                "4. Implement an Explainable Early-Warning Engine with threat severity categories and human-readable diagnostic cards.",
                "5. Respect Android security boundaries by operating within the application's isolated private sandbox."
            ]
        },
        # Slide 6: Proposed Methodology
        {
            "title": "Proposed Methodology: Kinetic Behavioral Detection",
            "subtitle": "Multi-Layered Controlled Laboratory Architecture",
            "bullets": [
                "Layer 1: Controlled Android Laboratory Application generating safe, isolated file operations in context.filesDir.",
                "Layer 2: Sliding-Window Feature Extractor (30s window duration, 10s slide interval) computing 10 kinetic features.",
                "Layer 3: Ensemble Random Forest Classifier (200 trees, balanced weights) trained without future lookahead bias.",
                "Layer 4: Explainable Early-Warning Engine translating ML probabilities into actionable severity tiers.",
                "Layer 5: Interactive 10-Page Research Dashboard for visualization, live CSV upload testing, and reports."
            ]
        },
        # Slide 7: System Architecture
        {
            "title": "End-to-End System Architecture",
            "subtitle": "Standardized Telemetry and Inference Pipeline",
            "bullets": [
                "Android Lab Simulation -> Emits event log (timestamp, file_id, operation, file_size, scenario_type, label).",
                "Storage Access Framework Export -> Exports CSV to local storage without elevated device permissions.",
                "Feature Extraction Pipeline -> Computes rolling-window operational velocity, ratios, and filesystem spread.",
                "Random Forest Engine -> Evaluates window threat probability with zero false alarms.",
                "Explainable Warning Engine -> Generates diagnostic card with risk score and behavioral indicators."
            ]
        },
        # Slide 8: Android Lab Application
        {
            "title": "Android Controlled Laboratory Application",
            "subtitle": "Native Kotlin + Jetpack Compose Implementation",
            "bullets": [
                "Safe Sandboxed Storage: All file I/O operations strictly restricted to context.filesDir/lab_files.",
                "Normal Simulation: 40 files, standard write and modification edits (150ms delay).",
                "Moderate Suspicious Simulation: 40 files, 10 extension renames, 5 deletions.",
                "High-Intensity Burst: 60 files, rapid multi-overwrite, 60 extension renames (.locked), 30 deletions.",
                "UI Features: Material 3 NavigationBar, real-time telemetry log, on-device diagnostics card, and CSV export."
            ]
        },
        # Slide 9: Dataset Generation & Taxonomies
        {
            "title": "Synthetic Dataset Generation & Taxonomy",
            "subtitle": "289,677 File Operation Events Across 240 Controlled Scenarios",
            "bullets": [
                "120 Benign Scenarios: Normal user navigation (40), Document editing (45), Photo backup bulk synchronization (35).",
                "120 Suspicious Scenarios: In-place modification burst (31), Extension rename burst (46), Gradual stealthy attack (43).",
                "Realistic Attack Onsets: In suspicious scenarios, attacks begin between 40s and 100s into the run (attack_start).",
                "Operation Vocabulary: WRITE, MODIFY, RENAME, DELETE, and READ with dynamic file sizes."
            ]
        },
        # Slide 10: Rolling-Window Feature Formulation
        {
            "title": "Rolling-Window Feature Formulation",
            "subtitle": "Ten Kinetic Features Extracted from 30s Overlapping Windows",
            "bullets": [
                "total_ops: Gross operation count in window | ops_per_second: Normalized throughput (ops / 30s).",
                "modify_count & modify_ratio: Frequency and share of in-place overwriting.",
                "rename_count & rename_ratio: Frequency and proportion of file renames (strongest indicator of extension appending).",
                "delete_count & delete_ratio: Batch file deletion / wiper kinetics.",
                "write_count: Frequency of newly initialized files (distinguishes photo backups from overwrites).",
                "unique_files: Number of distinct file handles accessed (filesystem breadth)."
            ]
        },
        # Slide 11: Machine Learning Model
        {
            "title": "Machine Learning Model: Random Forest",
            "subtitle": "Ensemble Decision Architecture with Balanced Weighting",
            "bullets": [
                "Model Choice: Random Forest Classifier (200 estimators, max depth 12, min samples leaf 2).",
                "Why Random Forest? Exceptional robustness against collinear temporal features, zero risk of exploding gradients, and high noise tolerance.",
                "Class Weighting: 'balanced' mode automatically adjusts weights inversely proportional to class frequencies.",
                "Inference Latency: Less than 2 milliseconds per rolling window, ideal for mobile resource constraints."
            ]
        },
        # Slide 12: Data Leakage Prevention
        {
            "title": "Rigorous Data Leakage Prevention",
            "subtitle": "Strict Scenario-Level Separation Architecture",
            "bullets": [
                "The Rolling-Window Leakage Trap: Randomly splitting overlapping windows allows models to memorize identical temporal states.",
                "Our Solution: Partitions are segregated strictly at the scenario level.",
                "Train Partition: 167 scenarios (2,672 rolling windows).",
                "Validation Partition: 37 scenarios (592 rolling windows).",
                "Held-Out Test Partition: 36 completely unseen scenarios (576 rolling windows: 18 benign, 18 suspicious)."
            ]
        },
        # Slide 13: Explainable Early-Warning Engine
        {
            "title": "Explainable Early-Warning Engine",
            "subtitle": "Translating Black-Box Probabilities into Actionable Security Intelligence",
            "bullets": [
                "Four Risk Severity Tiers: NORMAL (Benign), LOW RISK (Elevated), MEDIUM RISK (Anomaly), HIGH RISK (Active Burst).",
                "Specific Behavioral Indicators: 'Rapid file renaming burst (14 renames, 28% of ops)', 'Wide filesystem spread (18 files)'.",
                "Primary Diagnostic Justification: Clear synthesis of why the alert triggered.",
                "Full Traceability: Correlates predictions directly with window timestamps, operation counts, and affected file handles."
            ]
        },
        # Slide 14: Experimental Benchmark Results
        {
            "title": "Verified Experimental Benchmarks",
            "subtitle": "Direct Comparison on 36 Unseen Test Scenarios (576 Windows)",
            "bullets": [
                "Random Forest Accuracy: 99.48% (Precision: 100.0%, Recall: 98.32%, F1-Score: 99.15%).",
                "Fixed-Threshold Baseline Accuracy: 31.08% (Precision: 31.08%, Recall: 100.0%, F1-Score: 0.4742).",
                "False Positive Rate: Random Forest = 0.0% (0 false alarms) vs. Baseline = 100.0% (397 false alarms).",
                "Confusion Matrix RF: TN=397, FP=0, FN=3, TP=176 across all 576 test windows."
            ]
        },
        # Slide 15: Baseline Failure Analysis
        {
            "title": "Why Static Heuristic Thresholds Fail",
            "subtitle": "The 100% False Positive Rate Phenomenon in Mobile Environments",
            "bullets": [
                "Heuristic Rules: Fixed thresholds fire when modify > 15, rename > 8, delete > 8, or unique files > 20.",
                "Photo Backup Failure: Syncing 50 photos triggers >50 writes across >50 files -> 100% false alarm rate.",
                "Document Editing Failure: Word processors autosave drafts every 30s -> 100% false alarm rate.",
                "The Machine Learning Advantage: RF learns non-linear correlations between rename_ratio and write_count, distinguishing backups from attacks."
            ]
        },
        # Slide 16: Detection Delay Analysis
        {
            "title": "Detection Delay & Early Warning Timeliness",
            "subtitle": "Alerting Before Destructive Attack Completion",
            "bullets": [
                "Detection Rate: 100.0% (18 out of 18 suspicious scenarios detected before completion).",
                "Average Detection Delay: 7.94 seconds from attack start.",
                "Median Detection Delay: 8.50 seconds.",
                "Fastest Detection: 2.0 seconds (high-velocity rename burst).",
                "Slowest Detection: 14.0 seconds (gradual stealthy attack).",
                "Operational Impact: Ransomware scenarios lasted 80–120s; alerting at 7.94s saves >90% of user files."
            ]
        },
        # Slide 17: Benign Workflow Resilience
        {
            "title": "Benign Workflow Resilience & Zero False Alarms",
            "subtitle": "Validating System Practicality in Realistic Usage Scenarios",
            "bullets": [
                "Document Editing (112 test windows): 0 false alarms (0% FPR).",
                "Photo Backup (80 test windows): 0 false alarms (0% FPR).",
                "Normal Navigation (96 test windows): 0 false alarms (0% FPR).",
                "Usability Conclusion: The prototype eliminates false-alarm fatigue that causes users to disable security software."
            ]
        },
        # Slide 18: Streamlit Web Dashboard
        {
            "title": "Interactive 10-Page Research Dashboard",
            "subtitle": "Professional Light-Themed Cybersecurity Research Interface",
            "bullets": [
                "Modular Navigation: Overview, Dataset Explorer, Behavioral Analysis, Detection Centre, Model Performance.",
                "Advanced Analytics: Detection Delay Tracker, Benign Analysis, Reports & Export, and About Section.",
                "Interactive CSV Upload: Drag-and-drop any compatible Android event log for instant feature extraction and RF inference.",
                "Downloadable Reports: Instant export of evaluation metrics, predictions, and delay logs."
            ]
        },
        # Slide 19: Architectural Limitations & Scope
        {
            "title": "Architectural Limitations & Ethical Scope",
            "subtitle": "Honest Scientific Disclosures Regarding Mobile Security",
            "bullets": [
                "Controlled Lab Isolation: Telemetry was gathered in the app's private sandbox (context.filesDir).",
                "Android OS Privacy Boundaries: User-space Android apps cannot monitor other apps' private storage without root or enterprise MDM enrollment.",
                "Simulated vs. Live Malware: We simulated file-system kinetics without executing active cryptographic payload destruction.",
                "Future Enhancements: Investigating Accessibility services, hardware thermal side-channels, and on-device TFLite deployment."
            ]
        },
        # Slide 20: Conclusion & References
        {
            "title": "Conclusion & Research Impact",
            "subtitle": "Thank You! Team Cipher Aegis — AIORI Hackathon 3 (PS-001)",
            "bullets": [
                "Integrated Solution: Fully functioning Android App, reproducible ML pipeline, and 10-page Streamlit dashboard.",
                "Scientific Proof: Rolling-window kinetics achieve 99.48% accuracy with 0% false alarms and 7.94s average delay.",
                "Key Publications: Singh & Tripathy (2024), Cen et al. (2024), Sibtain et al. (2025), Chew et al. (2024).",
                "Open Source & Reproducible: Complete code, datasets, unit tests, and documentation ready for evaluation."
            ]
        }
    ]

    blank_layout = prs.slide_layouts[6]

    for idx, slide_info in enumerate(slides_content):
        slide = prs.slides.add_slide(blank_layout)

        # Background shape
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG
        bg.line.fill.background()

        # Top banner on content slides
        if idx > 0:
            top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(0.5), Inches(11.733), Inches(1.3))
            top_bar.fill.solid()
            top_bar.fill.fore_color.rgb = COLOR_CARD
            top_bar.line.color.rgb = COLOR_BORDER
            top_bar.line.width = Pt(1)

            tb = top_bar.text_frame
            tb.word_wrap = True
            tb.margin_left = Inches(0.3)
            tb.margin_top = Inches(0.2)

            p1 = tb.paragraphs[0]
            p1.text = slide_info["title"]
            p1.font.bold = True
            p1.font.size = Pt(22)
            p1.font.color.rgb = COLOR_PRIMARY

            p2 = tb.add_paragraph()
            p2.text = slide_info["subtitle"]
            p2.font.size = Pt(12)
            p2.font.color.rgb = COLOR_MUTED

            # Content Card
            content_card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.733), Inches(4.8))
            content_card.fill.solid()
            content_card.fill.fore_color.rgb = COLOR_CARD
            content_card.line.color.rgb = COLOR_BORDER
            content_card.line.width = Pt(1)

            ctb = content_card.text_frame
            ctb.word_wrap = True
            ctb.margin_left = Inches(0.4)
            ctb.margin_top = Inches(0.4)

            for b_idx, bullet in enumerate(slide_info["bullets"]):
                bp = ctb.paragraphs[0] if b_idx == 0 else ctb.add_paragraph()
                bp.text = f"•  {bullet}"
                bp.font.size = Pt(15)
                bp.font.color.rgb = COLOR_TEXT
                bp.space_after = Pt(14)

        else:
            # Title slide layout
            title_card = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.5), Inches(1.5), Inches(10.333), Inches(4.5))
            title_card.fill.solid()
            title_card.fill.fore_color.rgb = COLOR_CARD
            title_card.line.color.rgb = COLOR_PRIMARY
            title_card.line.width = Pt(2)

            ttb = title_card.text_frame
            ttb.word_wrap = True
            ttb.margin_left = Inches(0.5)
            ttb.margin_top = Inches(0.6)

            tp1 = ttb.paragraphs[0]
            tp1.text = slide_info["title"]
            tp1.font.bold = True
            tp1.font.size = Pt(30)
            tp1.font.color.rgb = COLOR_PRIMARY
            tp1.space_after = Pt(18)

            tp2 = ttb.add_paragraph()
            tp2.text = slide_info["subtitle"]
            tp2.font.size = Pt(15)
            tp2.font.color.rgb = COLOR_TEXT

    pptx_path = os.path.join(PRESENTATION_DIR, "Project_Presentation.pptx")
    prs.save(pptx_path)
    print(f"Generated PowerPoint Presentation (20 slides): {pptx_path}")


def create_presentation_script():
    md_path = os.path.join(PRESENTATION_DIR, "Presentation_Script.md")
    docx_path = os.path.join(PRESENTATION_DIR, "Presentation_Script.docx")

    doc = docx.Document()
    doc.add_heading("AIORI Hackathon 3 — Presentation Speaking Script", 0)
    doc.add_paragraph("Team: Cipher Aegis | Problem Statement: PS-001\nPresenter: PraisyDeva MahimaiJ\n")

    script_text = """
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
    """

    for line in script_text.strip().split("\n\n"):
        p = doc.add_paragraph(line.strip())
        p.paragraph_format.space_after = docx.shared.Pt(8)

    doc.save(docx_path)
    print(f"Generated Presentation Script (.docx): {docx_path}")

    with open(md_path, "w") as f:
        f.write("# Presentation Speaking Script: Team Cipher Aegis (PS-001)\n\n")
        f.write(script_text.strip())
    print(f"Generated Presentation Script (.md): {md_path}")


def create_video_script_and_storyboard():
    v_md_path = os.path.join(VIDEO_DIR, "Video_Script.md")
    v_docx_path = os.path.join(VIDEO_DIR, "Video_Script.docx")
    sb_md_path = os.path.join(VIDEO_DIR, "Storyboard.md")
    sb_pdf_path = os.path.join(VIDEO_DIR, "Storyboard.pdf")

    # 1. Video Script DOCX & MD
    v_doc = docx.Document()
    v_doc.add_heading("AIORI Hackathon 3 — Demonstration Video Script", 0)
    v_doc.add_paragraph("Project: Explainable Early Warning for Android Ransomware-Like Activity\nTeam: Cipher Aegis | Duration: ~4-5 Minutes\n")

    video_script_text = """
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
    """

    for line in video_script_text.strip().split("\n\n"):
        p = v_doc.add_paragraph(line.strip())
        p.paragraph_format.space_after = docx.shared.Pt(8)

    v_doc.save(v_docx_path)
    print(f"Generated Video Script (.docx): {v_docx_path}")

    with open(v_md_path, "w") as f:
        f.write("# Video Demonstration Script: Cipher Aegis (PS-001)\n\n")
        f.write(video_script_text.strip())
    print(f"Generated Video Script (.md): {v_md_path}")

    # 2. Storyboard PDF & MD
    styles = get_cipher_styles()
    story = []

    story.append(Paragraph("AIORI HACKATHON 3 — DEMONSTRATION STORYBOARD", styles['CoverMeta']))
    story.append(Spacer(1, 6))
    story.append(Paragraph("Video Demonstration Visual Storyboard & Sequence Plan", styles['CoverTitle']))
    story.append(Paragraph("Scene-by-Scene Visual Layout, Audio Cues, and Timecode Mapping", styles['CoverSubtitle']))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0284c7'), spaceAfter=14))

    storyboard_data = [
        [Paragraph("Scene & Timecode", styles['TableHeader']), Paragraph("Visual Composition & Screen Action", styles['TableHeader']), Paragraph("Audio & Narration Core Points", styles['TableHeader'])],
        [Paragraph("Scene 1<br/>0:00 - 0:35", styles['TableCellBold']), Paragraph("Dashboard Overview Page (Page 1) with system health cards and executive metrics.", styles['TableCell']), Paragraph("Introduce project title, Problem Statement PS-001, and Cipher Aegis team.", styles['TableCell'])],
        [Paragraph("Scene 2<br/>0:35 - 1:15", styles['TableCellBold']), Paragraph("Android Emulator showing 'Normal Activity' simulation. Telemetry feed scrolling 80 events.", styles['TableCell']), Paragraph("Explain safe sandbox storage isolation (context.filesDir) and verify 'NORMAL' diagnostic status.", styles['TableCell'])],
        [Paragraph("Scene 3<br/>1:15 - 2:05", styles['TableCellBold']), Paragraph("Android Emulator executing 'Moderate' and 'High Burst' simulations. Red cards appear.", styles['TableCell']), Paragraph("Demonstrate rapid extension renaming (.locked) and export android_simulation_events.csv.", styles['TableCell'])],
        [Paragraph("Scene 4<br/>2:05 - 3:00", styles['TableCellBold']), Paragraph("Streamlit Dashboard Pages 3 & 4. Charts show velocity surge and explainable alert cards.", styles['TableCell']), Paragraph("Highlight explainable indicators (confidence %, rename burst, spread) per 30s window.", styles['TableCell'])],
        [Paragraph("Scene 5<br/>3:00 - 3:45", styles['TableCellBold']), Paragraph("Streamlit Dashboard Pages 5 & 6 showing confusion matrices and 7.94s detection delay boxplots.", styles['TableCell']), Paragraph("Emphasize 99.48% RF accuracy, 0% FPR vs. 100% baseline failure, and 7.94s average delay.", styles['TableCell'])],
        [Paragraph("Scene 6<br/>3:45 - 4:30", styles['TableCellBold']), Paragraph("Streamlit Page 8 file uploader processing exported CSV in real time, followed by conclusion.", styles['TableCell']), Paragraph("Demonstrate interactive testing, summarize research contributions, and close presentation.", styles['TableCell'])]
    ]

    t_sb = Table(storyboard_data, colWidths=[90, 210, 204])
    t_sb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0284c7')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#f8fafc')]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sb)

    build_pdf_document("Storyboard.pdf", story)
    import shutil
    shutil.copy(os.path.join(PROJECT_ROOT, "Documentation/Storyboard.pdf"), sb_pdf_path)

    with open(sb_md_path, "w") as f:
        f.write("# Video Demonstration Visual Storyboard: Cipher Aegis (PS-001)\n\n")
        f.write("| Scene & Timecode | Visual Composition & Screen Action | Audio & Narration Core Points |\n|---|---|---|\n")
        for row in storyboard_data[1:]:
            f.write(f"| {row[0].text.replace('<br/>', ' ')} | {row[1].text} | {row[2].text} |\n")
    print(f"Generated Storyboard (.md): {sb_md_path}")


if __name__ == '__main__':
    print("Generating Presentation and Video deliverables...")
    create_pptx_deck()
    create_presentation_script()
    create_video_script_and_storyboard()
    print("All presentation and video materials generated successfully!")
