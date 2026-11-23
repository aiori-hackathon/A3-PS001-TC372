"""
Model Training Pipeline for Android Ransomware Early Warning.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Trains a Random Forest classifier on scenario-partitioned rolling-window features.
Preserves hyperparameters, saves artifacts, and evaluates cross-scenario generalization.
"""

import os
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score,
    accuracy_score,
    f1_score,
    precision_score,
    recall_score
)

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


def train_early_warning_model(
    train_csv_path: str,
    val_csv_path: str,
    model_output_dir: str,
    n_estimators: int = 200,
    max_depth: int = 12,
    min_samples_leaf: int = 2,
    random_state: int = 42
) -> RandomForestClassifier:
    """
    Trains the Random Forest model and persists model + feature column artifacts.
    """
    train_df = pd.read_csv(train_csv_path)
    val_df = pd.read_csv(val_csv_path)

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df['label']

    X_val = val_df[FEATURE_COLUMNS]
    y_val = val_df['label']

    print(f"Training Random Forest on {len(X_train)} samples across {train_df['scenario_id'].nunique()} scenarios...")
    print(f"Class distribution: {y_train.value_counts().to_dict()}")

    model = RandomForestClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        class_weight='balanced',
        random_state=random_state,
        n_jobs=-1
    )

    model.fit(X_train, y_train)

    # Validation evaluation
    val_preds = model.predict(X_val)
    val_probs = model.predict_proba(X_val)[:, 1]

    val_acc = accuracy_score(y_val, val_preds)
    val_prec = precision_score(y_val, val_preds, zero_division=0)
    val_rec = recall_score(y_val, val_preds, zero_division=0)
    val_f1 = f1_score(y_val, val_preds, zero_division=0)
    val_auc = roc_auc_score(y_val, val_probs)

    print("\n=== Validation Set Performance (37 unseen scenarios) ===")
    print(f"Accuracy:  {val_acc:.4f}")
    print(f"Precision: {val_prec:.4f}")
    print(f"Recall:    {val_rec:.4f}")
    print(f"F1-Score:  {val_f1:.4f}")
    print(f"ROC-AUC:   {val_auc:.4f}")
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_val, val_preds))

    # Save artifacts
    os.makedirs(model_output_dir, exist_ok=True)
    model_path = os.path.join(model_output_dir, 'random_forest.pkl')
    cols_path = os.path.join(model_output_dir, 'feature_columns.pkl')

    joblib.dump(model, model_path)
    joblib.dump(FEATURE_COLUMNS, cols_path)

    print(f"\nModel artifacts persisted:")
    print(f"  Model -> {model_path}")
    print(f"  Feature Columns -> {cols_path}")

    # Feature importances
    print("\nFeature Importances:")
    importances = model.feature_importances_
    sorted_idx = np.argsort(importances)[::-1]
    for i in sorted_idx:
        print(f"  {FEATURE_COLUMNS[i]:<16}: {importances[i]:.4f}")

    return model


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    tr_path = os.path.join(base_dir, 'data/processed/train.csv')
    v_path = os.path.join(base_dir, 'data/processed/validation.csv')
    m_dir = os.path.join(base_dir, 'models')

    train_early_warning_model(tr_path, v_path, m_dir)
