"""
Dataset Preprocessing and Scenario-Level Partitioning Module.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Handles schema validation, missing-value audits, duplicate identification,
and strict scenario-level partitioning to prevent data leakage across rolling windows.
"""

import os
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List

EXPECTED_EVENT_COLUMNS = [
    'scenario_id', 'timestamp', 'app_id', 'file_id',
    'operation', 'file_type', 'file_size', 'label', 'scenario_type'
]

EXPECTED_FEATURE_COLUMNS = [
    'scenario_id', 'scenario_type', 'window_start', 'window_end',
    'attack_start', 'total_ops', 'modify_count', 'rename_count',
    'delete_count', 'write_count', 'unique_files', 'ops_per_second',
    'modify_ratio', 'rename_ratio', 'delete_ratio', 'label'
]

MODEL_FEATURE_NAMES = [
    'total_ops', 'modify_count', 'rename_count', 'delete_count',
    'write_count', 'unique_files', 'ops_per_second',
    'modify_ratio', 'rename_ratio', 'delete_ratio'
]


EXPECTED_ANDROID_COLUMNS = [
    'timestamp', 'file_id', 'operation', 'file_size', 'scenario_type', 'label'
]


def audit_android_events_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs audit on Android laboratory telemetry export.
    Matches schema: [timestamp, file_id, operation, file_size, scenario_type, label]
    """
    missing_cols = [c for c in EXPECTED_ANDROID_COLUMNS if c not in df.columns]
    null_counts = df.isnull().sum().to_dict()
    total_records = len(df)
    unique_files = int(df['file_id'].nunique()) if 'file_id' in df.columns else 0
    operations_dist = df['operation'].value_counts().to_dict() if 'operation' in df.columns else {}
    label_dist = df['label'].value_counts().to_dict() if 'label' in df.columns else {}

    return {
        'total_records': total_records,
        'unique_files': unique_files,
        'missing_columns': missing_cols,
        'null_counts': null_counts,
        'operations_distribution': operations_dist,
        'label_distribution': label_dist,
        'is_valid': len(missing_cols) == 0
    }


def audit_events_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive data health audit on raw event logs.
    """
    missing_cols = [c for c in EXPECTED_EVENT_COLUMNS if c not in df.columns]
    null_counts = df.isnull().sum().to_dict()
    duplicate_count = int(df.duplicated().sum())
    total_records = len(df)
    unique_scenarios = int(df['scenario_id'].nunique()) if 'scenario_id' in df.columns else 0
    unique_files = int(df['file_id'].nunique()) if 'file_id' in df.columns else 0
    operations_dist = df['operation'].value_counts().to_dict() if 'operation' in df.columns else {}
    label_dist = df['label'].value_counts().to_dict() if 'label' in df.columns else {}
    
    return {
        'total_records': total_records,
        'unique_scenarios': unique_scenarios,
        'unique_files': unique_files,
        'missing_columns': missing_cols,
        'null_counts': null_counts,
        'duplicate_count': duplicate_count,
        'operations_distribution': operations_dist,
        'label_distribution': label_dist,
        'is_valid': len(missing_cols) == 0
    }


def audit_features_dataframe(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Performs comprehensive data health audit on extracted feature dataset.
    """
    missing_cols = [c for c in EXPECTED_FEATURE_COLUMNS if c not in df.columns]
    missing_model_features = [c for c in MODEL_FEATURE_NAMES if c not in df.columns]
    null_counts = df[MODEL_FEATURE_NAMES].isnull().sum().to_dict() if not missing_model_features else {}
    total_windows = len(df)
    unique_scenarios = int(df['scenario_id'].nunique()) if 'scenario_id' in df.columns else 0
    label_dist = df['label'].value_counts().to_dict() if 'label' in df.columns else {}
    
    return {
        'total_windows': total_windows,
        'unique_scenarios': unique_scenarios,
        'missing_columns': missing_cols,
        'missing_model_features': missing_model_features,
        'null_feature_counts': null_counts,
        'label_distribution': label_dist,
        'is_valid': len(missing_cols) == 0 and len(missing_model_features) == 0
    }


def partition_by_scenario(
    features_df: pd.DataFrame,
    test_scenario_ids: List[str],
    val_ratio: float = 0.1765,  # 36 / 204 ≈ 0.1765 yields 36 val and 168 train (70 / 15 / 15 split)
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Performs scenario-level separation ensuring zero overlap across train, validation, and test sets.
    Preserves historical benchmark test scenarios for rigorous comparability.
    """
    test_df = features_df[features_df['scenario_id'].isin(test_scenario_ids)].copy()
    remaining_df = features_df[~features_df['scenario_id'].isin(test_scenario_ids)].copy()
    
    remaining_scenarios = sorted(remaining_df['scenario_id'].unique())
    
    # Stratified scenario selection based on scenario type
    scenario_metadata = remaining_df.groupby('scenario_id')['scenario_type'].first()
    
    np.random.seed(random_state)
    val_scenarios = []
    
    for stype, group in scenario_metadata.groupby(scenario_metadata):
        s_list = group.index.tolist()
        n_val = max(1, int(round(len(s_list) * val_ratio)))
        selected = np.random.choice(s_list, size=n_val, replace=False).tolist()
        val_scenarios.extend(selected)
        
    train_scenarios = [s for s in remaining_scenarios if s not in val_scenarios]
    
    val_df = remaining_df[remaining_df['scenario_id'].isin(val_scenarios)].copy()
    train_df = remaining_df[remaining_df['scenario_id'].isin(train_scenarios)].copy()
    
    return train_df, val_df, test_df


def save_processed_splits(
    features_path: str,
    test_predictions_path: str,
    output_dir: str
) -> Dict[str, str]:
    """
    Loads features and test predictions, partitions by scenario, and saves split CSVs.
    """
    features_df = pd.read_csv(features_path)
    test_pred_df = pd.read_csv(test_predictions_path)
    
    test_scenarios = sorted(test_pred_df['scenario_id'].unique().tolist())
    train_df, val_df, test_df = partition_by_scenario(features_df, test_scenarios)
    
    os.makedirs(output_dir, exist_ok=True)
    train_path = os.path.join(output_dir, 'train.csv')
    val_path = os.path.join(output_dir, 'validation.csv')
    test_path = os.path.join(output_dir, 'test.csv')
    
    train_df.to_csv(train_path, index=False)
    val_df.to_csv(val_path, index=False)
    test_df.to_csv(test_path, index=False)
    
    return {
        'train': train_path,
        'validation': val_path,
        'test': test_path
    }


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    f_path = os.path.join(base_dir, 'data/processed/features.csv')
    tp_path = os.path.join(base_dir, 'results/test_predictions.csv')
    out_dir = os.path.join(base_dir, 'data/processed')
    
    splits = save_processed_splits(f_path, tp_path, out_dir)
    print("Partitioned splits saved successfully:")
    for k, v in splits.items():
        df = pd.read_csv(v)
        print(f"  {k}: {df.shape[0]} windows, {df['scenario_id'].nunique()} scenarios -> {v}")
