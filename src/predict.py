"""
Inference and Early-Warning Prediction Interface.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Provides batch and single-file prediction routines for Android file activity logs.
Generates early-warning risk assessments and explainability diagnostics.
"""

import os
import sys
import argparse
import joblib
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional

try:
    from .feature_extraction import extract_window_features, FEATURE_COLUMNS
    from .explainability import ExplainableWarningEngine, explain_scenario_dataframe
except ImportError:
    from feature_extraction import extract_window_features, FEATURE_COLUMNS
    from explainability import ExplainableWarningEngine, explain_scenario_dataframe


class EarlyWarningPredictor:
    """
    Inference engine that wraps model prediction with rolling-window extraction and explainability.
    """

    def __init__(self, model_path: str, columns_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(columns_path):
            raise FileNotFoundError(f"Columns file not found: {columns_path}")

        self.model = joblib.load(model_path)
        self.feature_columns = joblib.load(columns_path)

    def predict_features_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Runs model inference on pre-extracted rolling-window features DataFrame.
        """
        df_out = df.copy()
        missing = [c for c in self.feature_columns if c not in df_out.columns]
        if missing:
            raise ValueError(f"Input DataFrame is missing required features: {missing}")

        X = df_out[self.feature_columns]
        df_out['rf_prediction'] = self.model.predict(X)
        df_out['rf_probability'] = np.round(self.model.predict_proba(X)[:, 1], 4)

        # Baseline comparison
        def baseline(row):
            score = 0
            if row['modify_count'] > 15: score += 2
            if row['rename_count'] > 8: score += 2
            if row['delete_count'] > 8: score += 2
            if row['unique_files'] > 20: score += 2
            return int(score >= 2)

        df_out['baseline_prediction'] = df_out.apply(baseline, axis=1)

        # Generate explainable diagnostics
        diagnostics = explain_scenario_dataframe(
            df_out,
            df_out['rf_prediction'].values,
            df_out['rf_probability'].values
        )

        df_out['severity_level'] = [d['severity_level'] for d in diagnostics]
        df_out['primary_reason'] = [d['primary_reason'] for d in diagnostics]
        return df_out

    def predict_raw_events_csv(
        self,
        events_csv_path: str,
        window_duration: float = 30.0,
        slide_interval: float = 10.0
    ) -> pd.DataFrame:
        """
        End-to-end processing: raw event CSV -> rolling window -> inference -> explainability.
        """
        events_df = pd.read_csv(events_csv_path)

        # Accommodate Android schema
        if 'scenario_id' not in events_df.columns:
            events_df['scenario_id'] = 'SIM_SCENARIO'
        if 'attack_start' not in events_df.columns:
            events_df['attack_start'] = np.nan
        if 'file_type' not in events_df.columns:
            events_df['file_type'] = 'unknown'

        features_df = extract_window_features(
            events_df,
            window_duration_seconds=window_duration,
            slide_interval_seconds=slide_interval
        )

        return self.predict_features_dataframe(features_df)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Predict ransomware-like activity from event logs")
    parser.add_argument("--input", required=True, help="Path to input CSV (raw events or extracted features)")
    parser.add_argument("--is_raw", action="store_true", help="Set flag if input is raw event log")
    parser.add_argument("--output", default="predictions_output.csv", help="Output path for predictions CSV")

    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    m_path = os.path.join(base_dir, 'models/random_forest.pkl')
    c_path = os.path.join(base_dir, 'models/feature_columns.pkl')

    predictor = EarlyWarningPredictor(m_path, c_path)

    if args.is_raw:
        res = predictor.predict_raw_events_csv(args.input)
    else:
        df_in = pd.read_csv(args.input)
        res = predictor.predict_features_dataframe(df_in)

    res.to_csv(args.output, index=False)
    print(f"Predictions saved to {args.output}")
    print(f"Total windows: {len(res)}, Suspicious windows: {(res['rf_prediction'] == 1).sum()}")
