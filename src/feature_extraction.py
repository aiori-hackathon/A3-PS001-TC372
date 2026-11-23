"""
Feature Extraction Module for Android Ransomware Early Warning Prototype.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Extracts rolling-window behavioral features from file-operation event logs.
Preserves chronological integrity and prevents future-data leakage.
"""

import pandas as pd
import numpy as np
from datetime import timedelta
from typing import List, Dict, Optional, Tuple

FEATURE_COLUMNS = [
    'total_ops',
    'modify_count',
    'rename_count',
    'delete_count',
    'write_count',
    'unique_files',
    'ops_per_second',
    'modify_ratio',
    'rename_ratio',
    'delete_ratio'
]


def extract_window_features(
    events_df: pd.DataFrame,
    window_duration_seconds: float = 30.0,
    slide_interval_seconds: float = 10.0,
    timestamp_col: str = 'timestamp',
    operation_col: str = 'operation',
    file_id_col: str = 'file_id',
    label_col: str = 'label',
    scenario_id_col: str = 'scenario_id',
    scenario_type_col: str = 'scenario_type',
    attack_start_col: str = 'attack_start'
) -> pd.DataFrame:
    """
    Extracts overlapping rolling-window features across all scenarios in an event dataset.
    
    Args:
        events_df: DataFrame containing raw file-operation events.
        window_duration_seconds: Duration of each sliding window (default: 30.0s).
        slide_interval_seconds: Step size between window starts (default: 10.0s).
    
    Returns:
        DataFrame of rolling-window behavioral features.
    """
    if events_df.empty:
        return pd.DataFrame(columns=[
            'scenario_id', 'scenario_type', 'window_start', 'window_end',
            'attack_start'] + FEATURE_COLUMNS + ['label'])

    df = events_df.copy()
    
    # Auto-populate scenario_id if missing
    if scenario_id_col not in df.columns:
        if scenario_type_col in df.columns:
            df[scenario_id_col] = df[scenario_type_col]
        else:
            df[scenario_id_col] = 'SIM_SCENARIO'

    if attack_start_col not in df.columns:
        df[attack_start_col] = np.nan

    df[timestamp_col] = pd.to_datetime(df[timestamp_col])
    df = df.sort_values([scenario_id_col, timestamp_col])
    
    records = []
    grouped = df.groupby(scenario_id_col)
    
    for scenario_id, group in grouped:
        stype = group[scenario_type_col].iloc[0] if scenario_type_col in group.columns else 'unknown'
        
        attack_start_val = None
        if attack_start_col in group.columns and group[attack_start_col].notna().any():
            attack_start_val = str(group[attack_start_col].dropna().iloc[0])
            
        t_min = group[timestamp_col].min()
        t_max = group[timestamp_col].max()
        duration_total = (t_max - t_min).total_seconds()
        
        window_start = t_min
        
        # If scenario duration is shorter than window duration, generate at least one representative window
        if duration_total < window_duration_seconds:
            window_end = window_start + timedelta(seconds=window_duration_seconds)
            w_events = group
            total_ops = len(w_events)
            ops = w_events[operation_col].astype(str).str.upper()
            modify_c = int((ops == 'MODIFY').sum())
            rename_c = int((ops == 'RENAME').sum())
            delete_c = int((ops == 'DELETE').sum())
            write_c = int((ops == 'WRITE').sum())
            unique_f = int(w_events[file_id_col].nunique())
            ops_sec = round(total_ops / window_duration_seconds, 4)
            
            mod_r = round(modify_c / total_ops, 6) if total_ops > 0 else 0.0
            ren_r = round(rename_c / total_ops, 6) if total_ops > 0 else 0.0
            del_r = round(delete_c / total_ops, 6) if total_ops > 0 else 0.0
            w_label = int(w_events[label_col].max()) if label_col in w_events.columns else 0
            
            records.append({
                'scenario_id': scenario_id,
                'scenario_type': stype,
                'window_start': window_start.strftime('%Y-%m-%d %H:%M:%S'),
                'window_end': window_end.strftime('%Y-%m-%d %H:%M:%S'),
                'attack_start': attack_start_val,
                'total_ops': total_ops,
                'modify_count': modify_c,
                'rename_count': rename_c,
                'delete_count': delete_c,
                'write_count': write_c,
                'unique_files': unique_f,
                'ops_per_second': ops_sec,
                'modify_ratio': mod_r,
                'rename_ratio': ren_r,
                'delete_ratio': del_r,
                'label': w_label
            })
            continue

        while window_start + timedelta(seconds=window_duration_seconds) <= t_max + timedelta(seconds=slide_interval_seconds):
            window_end = window_start + timedelta(seconds=window_duration_seconds)
            
            # Select events strictly within [window_start, window_end)
            w_events = group[(group[timestamp_col] >= window_start) & (group[timestamp_col] < window_end)]
            total_ops = len(w_events)
            
            if total_ops == 0:
                record = {
                    'scenario_id': scenario_id,
                    'scenario_type': stype,
                    'window_start': window_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'window_end': window_end.strftime('%Y-%m-%d %H:%M:%S'),
                    'attack_start': attack_start_val,
                    'total_ops': 0,
                    'modify_count': 0,
                    'rename_count': 0,
                    'delete_count': 0,
                    'write_count': 0,
                    'unique_files': 0,
                    'ops_per_second': 0.0,
                    'modify_ratio': 0.0,
                    'rename_ratio': 0.0,
                    'delete_ratio': 0.0,
                    'label': 0
                }
            else:
                ops = w_events[operation_col].astype(str).str.upper()
                modify_c = int((ops == 'MODIFY').sum())
                rename_c = int((ops == 'RENAME').sum())
                delete_c = int((ops == 'DELETE').sum())
                write_c = int((ops == 'WRITE').sum())
                unique_f = int(w_events[file_id_col].nunique())
                ops_sec = round(total_ops / window_duration_seconds, 4)
                
                mod_r = round(modify_c / total_ops, 6)
                ren_r = round(rename_c / total_ops, 6)
                del_r = round(delete_c / total_ops, 6)
                w_label = int(w_events[label_col].max()) if label_col in w_events.columns else 0
                
                record = {
                    'scenario_id': scenario_id,
                    'scenario_type': stype,
                    'window_start': window_start.strftime('%Y-%m-%d %H:%M:%S'),
                    'window_end': window_end.strftime('%Y-%m-%d %H:%M:%S'),
                    'attack_start': attack_start_val,
                    'total_ops': total_ops,
                    'modify_count': modify_c,
                    'rename_count': rename_c,
                    'delete_count': delete_c,
                    'write_count': write_c,
                    'unique_files': unique_f,
                    'ops_per_second': ops_sec,
                    'modify_ratio': mod_r,
                    'rename_ratio': ren_r,
                    'delete_ratio': del_r,
                    'label': w_label
                }
                
            records.append(record)
            window_start += timedelta(seconds=slide_interval_seconds)
            
    return pd.DataFrame(records)
