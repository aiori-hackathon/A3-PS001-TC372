"""
End-to-End System Integration Test Suite.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Validates the full data pipeline:
Android CSV Export -> Validation -> Rolling-Window Extraction -> Random Forest Inference -> Explainable Alerts.
"""

import os
import sys
import unittest
import pandas as pd
import numpy as np

# Add ML/src to path
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ml_src = os.path.join(base_dir, "ML/src")
if ml_src not in sys.path:
    sys.path.insert(0, ml_src)

from feature_extraction import extract_window_features, FEATURE_COLUMNS
from explainability import ExplainableWarningEngine
from predict import EarlyWarningPredictor
from preprocessing import audit_events_dataframe, audit_features_dataframe, audit_android_events_dataframe


class TestEndToEndPipeline(unittest.TestCase):

    def setUp(self):
        self.base_dir = base_dir
        self.android_csv = os.path.join(base_dir, "ML/data/raw/android_simulation_events.csv")
        self.model_path = os.path.join(base_dir, "ML/models/random_forest.pkl")
        self.cols_path = os.path.join(base_dir, "ML/models/feature_columns.pkl")
        self.predictor = EarlyWarningPredictor(self.model_path, self.cols_path)

    def test_01_android_csv_audit(self):
        """Verifies Android export CSV conforms to required schema."""
        self.assertTrue(os.path.exists(self.android_csv), "Android CSV must exist")
        df = pd.read_csv(self.android_csv)
        self.assertGreater(len(df), 0, "Android events CSV should not be empty")

        audit = audit_android_events_dataframe(df)
        self.assertEqual(len(audit['missing_columns']), 0, f"Missing columns in Android CSV: {audit['missing_columns']}")
        self.assertIn('normal_activity', df['scenario_type'].values)
        self.assertIn('moderate_suspicious', df['scenario_type'].values)
        self.assertIn('high_intensity_suspicious', df['scenario_type'].values)

    def test_02_rolling_window_extraction(self):
        """Tests rolling-window feature extraction on Android simulation events."""
        df = pd.read_csv(self.android_csv)
        features_df = extract_window_features(
            df,
            window_duration_seconds=30.0,
            slide_interval_seconds=10.0
        )
        self.assertGreater(len(features_df), 0, "Extracted features should not be empty")

        for col in FEATURE_COLUMNS:
            self.assertIn(col, features_df.columns, f"Feature column {col} missing from output")

        # Verify no NaN values in features
        null_counts = features_df[FEATURE_COLUMNS].isnull().sum().sum()
        self.assertEqual(null_counts, 0, "No null values allowed in extracted features")

    def test_03_model_inference_and_explainability(self):
        """Tests live model prediction and explainable early-warning alert generation."""
        df = pd.read_csv(self.android_csv)
        predictions_df = self.predictor.predict_raw_events_csv(self.android_csv)

        self.assertIn('rf_prediction', predictions_df.columns)
        self.assertIn('rf_probability', predictions_df.columns)
        self.assertIn('severity_level', predictions_df.columns)
        self.assertIn('primary_reason', predictions_df.columns)

        # Check normal activity windows
        normal_windows = predictions_df[predictions_df['scenario_type'] == 'normal_activity']
        if not normal_windows.empty:
            # Normal activity should not trigger high risk
            high_risks = (normal_windows['severity_level'] == 'HIGH RISK').sum()
            self.assertEqual(high_risks, 0, "Normal activity must not produce HIGH RISK alerts")

        # Check high intensity windows
        high_windows = predictions_df[predictions_df['scenario_type'] == 'high_intensity_suspicious']
        if not high_windows.empty:
            # High intensity burst should trigger alert
            alerts = (high_windows['rf_prediction'] == 1).sum()
            self.assertGreater(alerts, 0, "High intensity burst must trigger at least one alert")

    def test_04_explainable_diagnostic_structure(self):
        """Tests the explainable engine output structure."""
        test_features = {
            'total_ops': 45,
            'modify_count': 20,
            'rename_count': 12,
            'delete_count': 6,
            'write_count': 7,
            'unique_files': 18,
            'ops_per_second': 1.5,
            'modify_ratio': 0.44,
            'rename_ratio': 0.27,
            'delete_ratio': 0.13
        }
        diag = ExplainableWarningEngine.evaluate_window(
            features=test_features,
            rf_prediction=1,
            rf_probability=0.98,
            timestamp="2026-11-23 20:00:00"
        )
        self.assertEqual(diag['severity_level'], "HIGH RISK")
        self.assertEqual(diag['prediction'], "Suspicious")
        self.assertGreater(len(diag['indicators']), 0)
        self.assertIn("renaming", diag['primary_reason'].lower())


if __name__ == '__main__':
    unittest.main()
