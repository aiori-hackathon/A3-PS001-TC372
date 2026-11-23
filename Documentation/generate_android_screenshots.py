"""
Cipher Aegis - Generate Pixel-Accurate Android Application Mockup Screenshots.
Faithfully renders the Jetpack Compose Material 3 UI from MainActivity.kt.
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = "/Users/praisydevamahimaij/Downloads/AIORI_PS001/Documentation/Screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color Palette (Material 3 Dark/Blue Theme from MainActivity.kt)
BG_COLOR = (15, 23, 42)        # #0f172a (Deep Slate)
SURFACE_COLOR = (30, 41, 59)   # #1e293b (Card Slate)
BORDER_COLOR = (51, 65, 85)    # #334155 (Subtle Border)
PRIMARY_BLUE = (2, 132, 199)   # #0284c7 (Cipher Accent Blue)
TEXT_WHITE = (248, 250, 252)   # #f8fafc (Pure Text)
TEXT_MUTED = (148, 163, 184)   # #94a3b8 (Secondary Text)
SUCCESS_GREEN = (34, 197, 94)  # #22c55e (Safe)
WARNING_AMBER = (245, 158, 11) # #f59e0b (Elevated)
DANGER_RED = (239, 68, 68)     # #ef4444 (Critical / High Risk)
CHIP_BG = (51, 65, 85)

WIDTH, HEIGHT = 450, 920

def create_base_phone_canvas():
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Status Bar
    draw.text((24, 14), "10:30", fill=TEXT_MUTED)
    draw.text((WIDTH - 70, 14), "5G  85%", fill=TEXT_MUTED)
    
    # Top App Bar
    draw.text((24, 48), "🛡️ Cipher Aegis Lab", fill=TEXT_WHITE)
    draw.text((24, 76), "Controlled Android Threat Simulator", fill=TEXT_MUTED)
    
    # Tab Row
    tab_y = 106
    draw.rectangle([20, tab_y, WIDTH - 20, tab_y + 40], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    
    return img, draw

def save_normal_screen():
    img, draw = create_base_phone_canvas()
    
    # Active Tab indicator (Tab 1: Simulation)
    draw.rectangle([22, 108, 150, 144], fill=PRIMARY_BLUE)
    draw.text((45, 118), "🧪 Simulation", fill=TEXT_WHITE)
    draw.text((170, 118), "🛡️ Diagnostics", fill=TEXT_MUTED)
    draw.text((310, 118), "ℹ️ About Lab", fill=TEXT_MUTED)
    
    # Sandbox Scope Banner
    draw.rounded_rectangle([20, 160, WIDTH - 20, 210], radius=8, fill=(12, 74, 110), outline=PRIMARY_BLUE, width=1)
    draw.text((32, 172), "🔒 STRICT SANDBOX ISOLATION", fill=(56, 189, 248))
    draw.text((32, 190), "Confined to context.filesDir/lab_files (Zero external impact)", fill=(186, 230, 253))
    
    # Scenario Selection
    draw.text((24, 226), "Select Simulation Scenario:", fill=TEXT_WHITE)
    
    # Option 1: Selected (Normal)
    draw.rounded_rectangle([20, 252, WIDTH - 20, 312], radius=8, fill=SURFACE_COLOR, outline=SUCCESS_GREEN, width=2)
    draw.ellipse([34, 272, 50, 288], fill=SUCCESS_GREEN)
    draw.text((64, 262), "Normal Activity (Benign)", fill=TEXT_WHITE)
    draw.text((64, 282), "Standard creation, editing & reading of 80 files", fill=TEXT_MUTED)
    
    # Option 2: Moderate
    draw.rounded_rectangle([20, 322, WIDTH - 20, 382], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.ellipse([34, 342, 50, 358], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((64, 332), "Moderate Suspicious Activity", fill=TEXT_WHITE)
    draw.text((64, 352), "Elevated write cadence, 15 renames to backup", fill=TEXT_MUTED)
    
    # Option 3: High
    draw.rounded_rectangle([20, 392, WIDTH - 20, 452], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.ellipse([34, 412, 50, 428], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((64, 402), "High-Intensity Burst (Crypto-Sim)", fill=TEXT_WHITE)
    draw.text((64, 422), "Rapid encryption simulation, 60 .locked, 30 del", fill=TEXT_MUTED)
    
    # Action Buttons
    draw.rounded_rectangle([20, 470, WIDTH - 20, 515], radius=8, fill=PRIMARY_BLUE)
    draw.text((150, 484), "▶ RUN BENIGN SIMULATION", fill=TEXT_WHITE)
    
    # Live Results Card
    draw.rounded_rectangle([20, 530, WIDTH - 20, 740], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((36, 546), "LAB TELEMETRY EXECUTION REPORT", fill=TEXT_WHITE)
    draw.line([36, 570, WIDTH - 36, 570], fill=BORDER_COLOR, width=1)
    
    # Metrics
    draw.text((36, 582), "Status:", fill=TEXT_MUTED)
    draw.rounded_rectangle([110, 578, 250, 602], radius=6, fill=(22, 101, 52))
    draw.text((120, 583), "NORMAL / BENIGN", fill=TEXT_WHITE)
    
    draw.text((36, 616), "Events Generated:  80 file operations", fill=TEXT_WHITE)
    draw.text((36, 640), "Breakdown:         W:40 | M:40 | R:0 | D:0", fill=TEXT_MUTED)
    draw.text((36, 664), "Kinetic Rate:      37.4 ops/second", fill=TEXT_MUTED)
    draw.text((36, 688), "Rolling Window:    30s Overlapping (10s Slide)", fill=TEXT_MUTED)
    draw.text((36, 712), "Anomaly Flag:      False (0 Rule Breaches)", fill=SUCCESS_GREEN)
    
    # Export CSV Button
    draw.rounded_rectangle([20, 755, WIDTH - 20, 800], radius=8, fill=SURFACE_COLOR, outline=PRIMARY_BLUE, width=1)
    draw.text((120, 770), "📥 EXPORT TELEMETRY CSV (80 ROWS)", fill=PRIMARY_BLUE)
    
    # Purge Storage Button
    draw.rounded_rectangle([20, 810, WIDTH - 20, 850], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((140, 822), "🗑️ PURGE LAB SANDBOX", fill=TEXT_MUTED)
    
    img.save(os.path.join(OUTPUT_DIR, "android_screen01_home_normal.png"))
    print("[+] Saved android_screen01_home_normal.png")

def save_moderate_screen():
    img, draw = create_base_phone_canvas()
    
    draw.rectangle([22, 108, 150, 144], fill=PRIMARY_BLUE)
    draw.text((45, 118), "🧪 Simulation", fill=TEXT_WHITE)
    draw.text((170, 118), "🛡️ Diagnostics", fill=TEXT_MUTED)
    draw.text((310, 118), "ℹ️ About Lab", fill=TEXT_MUTED)
    
    # Sandbox Scope Banner
    draw.rounded_rectangle([20, 160, WIDTH - 20, 210], radius=8, fill=(12, 74, 110), outline=PRIMARY_BLUE, width=1)
    draw.text((32, 172), "🔒 STRICT SANDBOX ISOLATION", fill=(56, 189, 248))
    draw.text((32, 190), "Confined to context.filesDir/lab_files (Zero external impact)", fill=(186, 230, 253))
    
    # Scenario Selection (Moderate Selected)
    draw.text((24, 226), "Select Simulation Scenario:", fill=TEXT_WHITE)
    
    draw.rounded_rectangle([20, 252, WIDTH - 20, 312], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.ellipse([34, 272, 50, 288], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((64, 262), "Normal Activity (Benign)", fill=TEXT_WHITE)
    draw.text((64, 282), "Standard creation, editing & reading of 80 files", fill=TEXT_MUTED)
    
    draw.rounded_rectangle([20, 322, WIDTH - 20, 382], radius=8, fill=SURFACE_COLOR, outline=WARNING_AMBER, width=2)
    draw.ellipse([34, 342, 50, 358], fill=WARNING_AMBER)
    draw.text((64, 332), "Moderate Suspicious Activity", fill=TEXT_WHITE)
    draw.text((64, 352), "Elevated write cadence, 15 renames to backup", fill=TEXT_WHITE)
    
    draw.rounded_rectangle([20, 392, WIDTH - 20, 452], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.ellipse([34, 412, 50, 428], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((64, 402), "High-Intensity Burst (Crypto-Sim)", fill=TEXT_WHITE)
    draw.text((64, 422), "Rapid encryption simulation, 60 .locked, 30 del", fill=TEXT_MUTED)
    
    draw.rounded_rectangle([20, 470, WIDTH - 20, 515], radius=8, fill=WARNING_AMBER)
    draw.text((140, 484), "▶ RUN MODERATE SIMULATION", fill=(15, 23, 42))
    
    # Results Card
    draw.rounded_rectangle([20, 530, WIDTH - 20, 740], radius=10, fill=SURFACE_COLOR, outline=WARNING_AMBER, width=1)
    draw.text((36, 546), "LAB TELEMETRY EXECUTION REPORT", fill=TEXT_WHITE)
    draw.line([36, 570, WIDTH - 36, 570], fill=BORDER_COLOR, width=1)
    
    draw.text((36, 582), "Status:", fill=TEXT_MUTED)
    draw.rounded_rectangle([110, 578, 280, 602], radius=6, fill=(146, 64, 14))
    draw.text((120, 583), "⚠️ MODERATE SUSPICIOUS", fill=TEXT_WHITE)
    
    draw.text((36, 616), "Events Generated:  95 file operations", fill=TEXT_WHITE)
    draw.text((36, 640), "Breakdown:         W:20 | M:60 | R:15 | D:0", fill=TEXT_MUTED)
    draw.text((36, 664), "Kinetic Rate:      44.8 ops/second", fill=TEXT_MUTED)
    draw.text((36, 688), "Diagnostic Note:   Renames observed (15.8% of ops)", fill=WARNING_AMBER)
    draw.text((36, 712), "Confidence Level:  Moderate Early Warning Flag", fill=TEXT_WHITE)
    
    draw.rounded_rectangle([20, 755, WIDTH - 20, 800], radius=8, fill=SURFACE_COLOR, outline=PRIMARY_BLUE, width=1)
    draw.text((120, 770), "📥 EXPORT TELEMETRY CSV (95 ROWS)", fill=PRIMARY_BLUE)
    
    draw.rounded_rectangle([20, 810, WIDTH - 20, 850], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((140, 822), "🗑️ PURGE LAB SANDBOX", fill=TEXT_MUTED)
    
    img.save(os.path.join(OUTPUT_DIR, "android_screen02_moderate_simulation.png"))
    print("[+] Saved android_screen02_moderate_simulation.png")

def save_high_attack_screen():
    img, draw = create_base_phone_canvas()
    
    draw.rectangle([22, 108, 150, 144], fill=PRIMARY_BLUE)
    draw.text((45, 118), "🧪 Simulation", fill=TEXT_WHITE)
    draw.text((170, 118), "🛡️ Diagnostics", fill=TEXT_MUTED)
    draw.text((310, 118), "ℹ️ About Lab", fill=TEXT_MUTED)
    
    # Sandbox Scope Banner
    draw.rounded_rectangle([20, 160, WIDTH - 20, 210], radius=8, fill=(12, 74, 110), outline=PRIMARY_BLUE, width=1)
    draw.text((32, 172), "🔒 STRICT SANDBOX ISOLATION", fill=(56, 189, 248))
    draw.text((32, 190), "Confined to context.filesDir/lab_files (Zero external impact)", fill=(186, 230, 253))
    
    # Scenario Selection (High Selected)
    draw.text((24, 226), "Select Simulation Scenario:", fill=TEXT_WHITE)
    
    draw.rounded_rectangle([20, 252, WIDTH - 20, 312], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.ellipse([34, 272, 50, 288], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((64, 262), "Normal Activity (Benign)", fill=TEXT_WHITE)
    draw.text((64, 282), "Standard creation, editing & reading of 80 files", fill=TEXT_MUTED)
    
    draw.rounded_rectangle([20, 322, WIDTH - 20, 382], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.ellipse([34, 342, 50, 358], fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((64, 332), "Moderate Suspicious Activity", fill=TEXT_WHITE)
    draw.text((64, 352), "Elevated write cadence, 15 renames to backup", fill=TEXT_MUTED)
    
    draw.rounded_rectangle([20, 392, WIDTH - 20, 452], radius=8, fill=SURFACE_COLOR, outline=DANGER_RED, width=2)
    draw.ellipse([34, 412, 50, 428], fill=DANGER_RED)
    draw.text((64, 402), "High-Intensity Burst (Crypto-Sim)", fill=TEXT_WHITE)
    draw.text((64, 422), "Rapid encryption simulation, 60 .locked, 30 del", fill=TEXT_WHITE)
    
    draw.rounded_rectangle([20, 470, WIDTH - 20, 515], radius=8, fill=DANGER_RED)
    draw.text((130, 484), "🚨 SIMULATE HIGH ATTACK BURST", fill=TEXT_WHITE)
    
    # Critical Alert Card
    draw.rounded_rectangle([20, 530, WIDTH - 20, 740], radius=10, fill=(69, 10, 10), outline=DANGER_RED, width=2)
    draw.text((36, 546), "🚨 CRITICAL EARLY WARNING ALERT", fill=(254, 202, 202))
    draw.line([36, 570, WIDTH - 36, 570], fill=DANGER_RED, width=1)
    
    draw.text((36, 582), "Classification:", fill=TEXT_MUTED)
    draw.rounded_rectangle([150, 578, 380, 602], radius=6, fill=DANGER_RED)
    draw.text((160, 583), "HIGH RISK (RANSOMWARE-LIKE)", fill=TEXT_WHITE)
    
    draw.text((36, 616), "Burst Metrics:    120 Ops across 60 Targets", fill=TEXT_WHITE)
    draw.text((36, 640), "Mass Extension:   60 files rewritten to *.locked", fill=(254, 202, 202))
    draw.text((36, 664), "Kinetic Velocity: 58.2 ops/sec (3.4x benign rate)", fill=(254, 202, 202))
    draw.text((36, 688), "Rolling Window:   Triggered at T = 8.5 seconds", fill=TEXT_WHITE)
    draw.text((36, 712), "Mitigation:       Telemetry logged. Export ready.", fill=SUCCESS_GREEN)
    
    draw.rounded_rectangle([20, 755, WIDTH - 20, 800], radius=8, fill=SURFACE_COLOR, outline=PRIMARY_BLUE, width=1)
    draw.text((115, 770), "📥 EXPORT TELEMETRY CSV (120 ROWS)", fill=PRIMARY_BLUE)
    
    draw.rounded_rectangle([20, 810, WIDTH - 20, 850], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((140, 822), "🗑️ PURGE LAB SANDBOX", fill=TEXT_MUTED)
    
    img.save(os.path.join(OUTPUT_DIR, "android_screen03_high_burst_attack.png"))
    print("[+] Saved android_screen03_high_burst_attack.png")

def save_diagnostics_screen():
    img, draw = create_base_phone_canvas()
    
    # Active Tab indicator (Tab 2: Diagnostics)
    draw.rectangle([150, 108, 290, 144], fill=PRIMARY_BLUE)
    draw.text((45, 118), "🧪 Simulation", fill=TEXT_MUTED)
    draw.text((170, 118), "🛡️ Diagnostics", fill=TEXT_WHITE)
    draw.text((310, 118), "ℹ️ About Lab", fill=TEXT_MUTED)
    
    # Diagnostic Overview Card
    draw.rounded_rectangle([20, 160, WIDTH - 20, 290], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((36, 175), "DIAGNOSTIC ENGINE STATUS", fill=TEXT_WHITE)
    draw.text((36, 200), "Engine Type:      Hybrid Rules + ML Feature Extractor", fill=TEXT_MUTED)
    draw.text((36, 222), "Window Duration:  30 seconds (Rolling)", fill=TEXT_MUTED)
    draw.text((36, 244), "Slide Step:       10 seconds overlap", fill=TEXT_MUTED)
    draw.text((36, 266), "Heuristic Check:  Active (Rename ratio > 0.35)", fill=TEXT_WHITE)
    
    # Feature Extraction Breakdown
    draw.text((24, 308), "Latest Window Behavioral Features:", fill=TEXT_WHITE)
    
    features = [
        ("Total Operations (total_ops)", "120 ops", DANGER_RED),
        ("Modification Ratio (modify_ratio)", "0.25", TEXT_WHITE),
        ("Rename Ratio (rename_ratio)", "0.50 (Critical)", DANGER_RED),
        ("Delete Ratio (delete_ratio)", "0.25", WARNING_AMBER),
        ("Operation Rate (ops_per_second)", "58.2 ops/s", DANGER_RED),
        ("Target File Entropy Count", "60 unique files", WARNING_AMBER),
    ]
    
    y = 336
    for name, val, col in features:
        draw.rounded_rectangle([20, y, WIDTH - 20, y + 54], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
        draw.text((36, y + 10), name, fill=TEXT_MUTED)
        draw.text((36, y + 30), val, fill=col)
        y += 62
        
    # Explainability Card
    draw.rounded_rectangle([20, y + 10, WIDTH - 20, y + 130], radius=10, fill=(30, 27, 75), outline=(99, 102, 241), width=1)
    draw.text((36, y + 25), "EXPLAINABILITY VERDICT", fill=(199, 210, 254))
    draw.text((36, y + 50), "High rename ratio (50%) and burst velocity (58.2/s)", fill=TEXT_WHITE)
    draw.text((36, y + 70), "diverge sharply from normal file modification baseline.", fill=TEXT_WHITE)
    draw.text((36, y + 92), "Recommended Action: Quarantine Process & Alert Admin", fill=(254, 202, 202))
    
    img.save(os.path.join(OUTPUT_DIR, "android_screen04_live_diagnostics.png"))
    print("[+] Saved android_screen04_live_diagnostics.png")

def save_about_screen():
    img, draw = create_base_phone_canvas()
    
    # Active Tab indicator (Tab 3: About Lab)
    draw.rectangle([290, 108, WIDTH - 22, 144], fill=PRIMARY_BLUE)
    draw.text((45, 118), "🧪 Simulation", fill=TEXT_MUTED)
    draw.text((170, 118), "🛡️ Diagnostics", fill=TEXT_MUTED)
    draw.text((310, 118), "ℹ️ About Lab", fill=TEXT_WHITE)
    
    # Project Identity Card
    draw.rounded_rectangle([20, 160, WIDTH - 20, 310], radius=10, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
    draw.text((36, 175), "CIPHER AEGIS RESEARCH LAB", fill=TEXT_WHITE)
    draw.text((36, 200), "Project:    Explainable Early Warning for Android", fill=TEXT_MUTED)
    draw.text((36, 222), "            Ransomware-Like Activity", fill=TEXT_MUTED)
    draw.text((36, 244), "Hackathon:  AIORI Hackathon 3 (Problem PS-001)", fill=TEXT_MUTED)
    draw.text((36, 266), "Lead Dev:   PraisyDeva MahimaiJ", fill=TEXT_WHITE)
    draw.text((36, 288), "Institute:  Karunya Institute of Technology & Sciences", fill=TEXT_MUTED)
    
    # Architectural Pillars
    draw.text((24, 328), "Controlled Lab Architecture:", fill=TEXT_WHITE)
    
    pillars = [
        ("1. Sandbox Confinement", "No shared external storage access; zero system file disruption."),
        ("2. Rolling-Window Dynamics", "30-second temporal windows with 10-second slide."),
        ("3. Random Forest Classification", "200 decision trees, depth 12, 99.48% test accuracy."),
        ("4. Transparent Explainability", "Severity tiers (Normal, Low, Med, High) with kinetic cards."),
        ("5. Academic Integrity", "All telemetry generated in controlled lab; ethical boundary enforced.")
    ]
    
    y = 356
    for title, desc in pillars:
        draw.rounded_rectangle([20, y, WIDTH - 20, y + 68], radius=8, fill=SURFACE_COLOR, outline=BORDER_COLOR, width=1)
        draw.text((36, y + 10), title, fill=(56, 189, 248))
        draw.text((36, y + 32), desc[:48], fill=TEXT_MUTED)
        draw.text((36, y + 48), desc[48:], fill=TEXT_MUTED)
        y += 76
        
    img.save(os.path.join(OUTPUT_DIR, "android_screen05_about_scope.png"))
    print("[+] Saved android_screen05_about_scope.png")

if __name__ == "__main__":
    save_normal_screen()
    save_moderate_screen()
    save_high_attack_screen()
    save_diagnostics_screen()
    save_about_screen()
    print("\n[+] All 5 Android App screenshots generated successfully.")
