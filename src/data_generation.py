"""
Reproducible Synthetic Event Dataset Generation Pipeline.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Generates varied, controlled file-operation scenarios for benign user workflows
and ransomware-like behavioral attacks within a safe simulation environment.
"""

import os
import random
import datetime
import pandas as pd
import numpy as np
from typing import List, Dict, Optional, Tuple


BENIGN_SCENARIOS = ['normal', 'document_editing', 'photo_backup']
SUSPICIOUS_SCENARIOS = ['modification_burst', 'rename_burst', 'gradual_activity']


class SyntheticDataGenerator:
    """
    Generator for synthetic file activity event streams in Android lab simulations.
    """

    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        random.seed(random_seed)
        np.random.seed(random_seed)

    def generate_scenario(
        self,
        scenario_id: str,
        scenario_type: str,
        start_time: datetime.datetime,
        duration_seconds: int = 180,
        n_apps: int = 5,
        n_files: int = 80
    ) -> Tuple[List[Dict], Optional[str]]:
        """
        Generates an event stream for a single scenario.
        """
        events = []
        app_pool = [f"APP_{i+1}" for i in range(n_apps)]
        file_pool = [f"doc_{i+1:03d}" for i in range(n_files)]
        file_extensions = {f: random.choice(['.docx', '.pdf', '.jpg', '.xlsx', '.txt']) for f in file_pool}
        file_sizes = {f: random.randint(1024, 204800) for f in file_pool}
        
        is_attack = scenario_type in SUSPICIOUS_SCENARIOS
        attack_start_time = None
        attack_start_str = None
        
        if is_attack:
            # Attack starts between 40s and 100s into the 180s scenario
            attack_offset = random.randint(40, 100)
            attack_start_time = start_time + datetime.timedelta(seconds=attack_offset)
            attack_start_str = attack_start_time.strftime("%Y-%m-%d %H:%M:%S")

        current_time = start_time
        end_time = start_time + datetime.timedelta(seconds=duration_seconds)

        while current_time < end_time:
            time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
            under_attack = (is_attack and current_time >= attack_start_time)

            if not under_attack:
                # Normal benign event generation
                app = random.choice(app_pool)
                f_id = random.choice(file_pool)
                ext = file_extensions[f_id]
                size = file_sizes[f_id]
                
                if scenario_type == 'document_editing':
                    op = random.choices(['WRITE', 'MODIFY', 'READ'], weights=[0.4, 0.45, 0.15])[0]
                    step = random.uniform(0.1, 0.5)
                elif scenario_type == 'photo_backup':
                    op = random.choices(['WRITE', 'READ', 'MODIFY'], weights=[0.65, 0.25, 0.10])[0]
                    step = random.uniform(0.05, 0.3)
                else:  # normal
                    op = random.choices(['WRITE', 'READ', 'MODIFY', 'RENAME', 'DELETE'], weights=[0.35, 0.30, 0.20, 0.08, 0.07])[0]
                    step = random.uniform(0.1, 0.6)

                events.append({
                    'scenario_id': scenario_id,
                    'timestamp': time_str,
                    'app_id': app,
                    'file_id': f"{f_id}{ext}",
                    'operation': op,
                    'file_type': ext.replace('.', ''),
                    'file_size': size,
                    'label': 0,
                    'scenario_type': scenario_type,
                    'attack_start': attack_start_str
                })
                current_time += datetime.timedelta(seconds=step)

            else:
                # Malicious ransomware-like event generation
                app = "APP_MALICIOUS" if random.random() < 0.7 else random.choice(app_pool)
                f_id = random.choice(file_pool)
                ext = file_extensions[f_id]
                size = file_sizes[f_id]

                if scenario_type == 'rename_burst':
                    # Rapid renaming pattern: .locked, .crypto, .enc
                    op = random.choices(['RENAME', 'MODIFY', 'WRITE', 'DELETE'], weights=[0.60, 0.25, 0.10, 0.05])[0]
                    renamed_ext = ext + ".locked" if op == 'RENAME' else ext
                    step = random.uniform(0.02, 0.15)
                    events.append({
                        'scenario_id': scenario_id,
                        'timestamp': time_str,
                        'app_id': app,
                        'file_id': f"{f_id}{renamed_ext}",
                        'operation': op,
                        'file_type': 'locked' if op == 'RENAME' else ext.replace('.', ''),
                        'file_size': size + 1024,
                        'label': 1,
                        'scenario_type': scenario_type,
                        'attack_start': attack_start_str
                    })

                elif scenario_type == 'modification_burst':
                    # In-place overwriting/encrypting
                    op = random.choices(['MODIFY', 'WRITE', 'RENAME', 'DELETE'], weights=[0.65, 0.20, 0.10, 0.05])[0]
                    step = random.uniform(0.02, 0.12)
                    events.append({
                        'scenario_id': scenario_id,
                        'timestamp': time_str,
                        'app_id': app,
                        'file_id': f"{f_id}{ext}",
                        'operation': op,
                        'file_type': ext.replace('.', ''),
                        'file_size': size,
                        'label': 1,
                        'scenario_type': scenario_type,
                        'attack_start': attack_start_str
                    })

                elif scenario_type == 'gradual_activity':
                    # Slower, stealthier modification and rename
                    op = random.choices(['MODIFY', 'RENAME', 'WRITE', 'DELETE'], weights=[0.40, 0.35, 0.15, 0.10])[0]
                    step = random.uniform(0.08, 0.35)
                    events.append({
                        'scenario_id': scenario_id,
                        'timestamp': time_str,
                        'app_id': app,
                        'file_id': f"{f_id}{ext}",
                        'operation': op,
                        'file_type': ext.replace('.', ''),
                        'file_size': size,
                        'label': 1,
                        'scenario_type': scenario_type,
                        'attack_start': attack_start_str
                    })

                current_time += datetime.timedelta(seconds=step)

        return events, attack_start_str

    def generate_full_synthetic_dataset(
        self,
        output_csv_path: str,
        n_scenarios_per_type: int = 40,
        duration_seconds: int = 180
    ) -> pd.DataFrame:
        """
        Generates a balanced full synthetic dataset across all 6 scenario types.
        """
        all_events = []
        base_date = datetime.datetime(2026, 1, 10, 10, 0, 0)
        s_count = 1

        for stype in BENIGN_SCENARIOS:
            for i in range(n_scenarios_per_type):
                sid = f"B{s_count:03d}"
                s_time = base_date + datetime.timedelta(hours=s_count * 2)
                evs, _ = self.generate_scenario(sid, stype, s_time, duration_seconds=duration_seconds)
                all_events.extend(evs)
                s_count += 1

        susp_count = 1
        for stype in SUSPICIOUS_SCENARIOS:
            for i in range(n_scenarios_per_type):
                sid = f"S{susp_count:03d}"
                s_time = base_date + datetime.timedelta(hours=(s_count + susp_count) * 2)
                evs, _ = self.generate_scenario(sid, stype, s_time, duration_seconds=duration_seconds)
                all_events.extend(evs)
                susp_count += 1

        df = pd.DataFrame(all_events)
        os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
        df.to_csv(output_csv_path, index=False)
        return df


def generate_android_lab_events(output_path: str) -> pd.DataFrame:
    """
    Simulates the exact event logs emitted by the Kotlin Android laboratory application
    for Normal, Moderate Suspicious, and High Intensity Suspicious simulations.
    Matches schema: [scenario_id, timestamp, file_id, operation, file_size, scenario_type, label]
    """
    events = []
    base_time = datetime.datetime.now() - datetime.timedelta(minutes=15)

    # 1. Normal Simulation (40 files, write + modify, normal 800ms pacing = 64s duration)
    cur = base_time
    for i in range(40):
        fname = f"lab_file_{i}.txt"
        cur += datetime.timedelta(milliseconds=800)
        events.append({
            'scenario_id': 'AND_NORM',
            'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'file_id': fname,
            'operation': 'write',
            'file_size': 32 + i * 2,
            'scenario_type': 'normal_activity',
            'label': 0
        })
        cur += datetime.timedelta(milliseconds=800)
        events.append({
            'scenario_id': 'AND_NORM',
            'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'file_id': fname,
            'operation': 'modify',
            'file_size': 56 + i * 2,
            'scenario_type': 'normal_activity',
            'label': 0
        })

    # 2. Moderate Suspicious Simulation (40 files, write + modify, 10 renames, 5 deletes)
    cur += datetime.timedelta(minutes=2)
    for i in range(40):
        fname = f"lab_file_{i}.txt"
        cur += datetime.timedelta(milliseconds=400)
        events.append({
            'scenario_id': 'AND_MOD',
            'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'file_id': fname,
            'operation': 'write',
            'file_size': 32 + i * 2,
            'scenario_type': 'moderate_suspicious',
            'label': 1
        })
        cur += datetime.timedelta(milliseconds=400)
        events.append({
            'scenario_id': 'AND_MOD',
            'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'file_id': fname,
            'operation': 'modify',
            'file_size': 64 + i * 2,
            'scenario_type': 'moderate_suspicious',
            'label': 1
        })
        if i < 10:
            renamed_name = f"renamed_lab_file_{i}.txt"
            cur += datetime.timedelta(milliseconds=200)
            events.append({
                'scenario_id': 'AND_MOD',
                'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'file_id': renamed_name,
                'operation': 'rename',
                'file_size': 64 + i * 2,
                'scenario_type': 'moderate_suspicious',
                'label': 1
            })
            if i < 5:
                cur += datetime.timedelta(milliseconds=200)
                events.append({
                    'scenario_id': 'AND_MOD',
                    'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                    'file_id': renamed_name,
                    'operation': 'delete',
                    'file_size': 0,
                    'scenario_type': 'moderate_suspicious',
                    'label': 1
                })

    # 3. High-Intensity Suspicious Simulation (60 files, write + 2 modifies, 60 renames, 30 deletes)
    cur += datetime.timedelta(minutes=2)
    for i in range(60):
        fname = f"lab_file_{i}.txt"
        cur += datetime.timedelta(milliseconds=150)
        events.append({
            'scenario_id': 'AND_HIGH',
            'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'file_id': fname,
            'operation': 'write',
            'file_size': 32 + i * 2,
            'scenario_type': 'high_intensity_suspicious',
            'label': 1
        })
        for m in range(2):
            cur += datetime.timedelta(milliseconds=150)
            events.append({
                'scenario_id': 'AND_HIGH',
                'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'file_id': fname,
                'operation': 'modify',
                'file_size': 80 + i * 2 + m * 20,
                'scenario_type': 'high_intensity_suspicious',
                'label': 1
            })
        renamed_name = f"renamed_lab_file_{i}.txt"
        cur += datetime.timedelta(milliseconds=100)
        events.append({
            'scenario_id': 'AND_HIGH',
            'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
            'file_id': renamed_name,
            'operation': 'rename',
            'file_size': 120 + i * 2,
            'scenario_type': 'high_intensity_suspicious',
            'label': 1
        })
        if i < 30:
            cur += datetime.timedelta(milliseconds=100)
            events.append({
                'scenario_id': 'AND_HIGH',
                'timestamp': cur.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                'file_id': renamed_name,
                'operation': 'delete',
                'file_size': 0,
                'scenario_type': 'high_intensity_suspicious',
                'label': 1
            })

    df = pd.DataFrame(events)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    return df


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    android_out = os.path.join(base_dir, 'data/raw/android_simulation_events.csv')
    df_sim = generate_android_lab_events(android_out)
    print(f"Generated Android simulation events ({len(df_sim)} rows) -> {android_out}")
    print(df_sim.groupby(['scenario_type', 'operation']).size())
