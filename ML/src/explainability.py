"""
Explainable Early-Warning Engine for Android Ransomware Behavioral Analysis.
AIORI Hackathon 3 | PS-001 | Team Cipher Aegis

Translates raw rolling-window features and machine learning model predictions
into actionable, human-interpretable security alerts and severity levels.
"""

from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np


class ExplainableWarningEngine:
    """
    Early-warning explainability engine that computes risk severity,
    identifies contributing behavioral indicators, and generates contextual explanations.
    """

    # Behavioral indicator thresholds
    RENAME_BURST_THRESHOLD = 5
    MODIFY_BURST_THRESHOLD = 15
    DELETE_BURST_THRESHOLD = 5
    HIGH_OPS_PER_SEC_THRESHOLD = 8.0
    HIGH_UNIQUE_FILES_THRESHOLD = 15
    SUSPICIOUS_RENAME_RATIO = 0.20
    SUSPICIOUS_MODIFY_RATIO = 0.40

    @classmethod
    def evaluate_window(
        cls,
        features: Dict[str, Any],
        rf_prediction: int,
        rf_probability: float,
        timestamp: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Evaluates a single rolling window and produces an explainable diagnostic card.
        
        Args:
            features: Dictionary containing rolling-window feature values.
            rf_prediction: Model classification (0 = Benign, 1 = Suspicious).
            rf_probability: Model suspicious class probability [0.0, 1.0].
            timestamp: Window end timestamp or detection time.
            
        Returns:
            Dictionary containing structured alert diagnostics.
        """
        modify_count = int(features.get('modify_count', 0))
        rename_count = int(features.get('rename_count', 0))
        delete_count = int(features.get('delete_count', 0))
        write_count = int(features.get('write_count', 0))
        total_ops = int(features.get('total_ops', 0))
        unique_files = int(features.get('unique_files', 0))
        ops_per_sec = float(features.get('ops_per_second', 0.0))
        rename_ratio = float(features.get('rename_ratio', 0.0))
        modify_ratio = float(features.get('modify_ratio', 0.0))
        delete_ratio = float(features.get('delete_ratio', 0.0))

        indicators: List[str] = []
        severity_score = 0.0

        # Indicator 1: Rename burst (hallmark of crypto-ransomware appending extensions)
        if rename_count >= cls.RENAME_BURST_THRESHOLD:
            indicators.append(
                f"Rapid file renaming burst ({rename_count} renames, {rename_ratio*100:.1f}% of window ops)"
            )
            severity_score += 3.0
        elif rename_count > 0 and rename_ratio >= cls.SUSPICIOUS_RENAME_RATIO:
            indicators.append(
                f"Elevated rename ratio ({rename_ratio*100:.1f}% of operations)"
            )
            severity_score += 1.5

        # Indicator 2: Modification burst (rapid in-place file encryption/tampering)
        if modify_count >= cls.MODIFY_BURST_THRESHOLD:
            indicators.append(
                f"High-frequency file modification ({modify_count} modifications, {modify_ratio*100:.1f}% of ops)"
            )
            severity_score += 2.5
        elif modify_count > 5 and modify_ratio >= cls.SUSPICIOUS_MODIFY_RATIO:
            indicators.append(
                f"Abnormal modification share ({modify_ratio*100:.1f}% of operations)"
            )
            severity_score += 1.5

        # Indicator 3: Deletion spike (wiper or ransomware cleanup)
        if delete_count >= cls.DELETE_BURST_THRESHOLD:
            indicators.append(
                f"Batch deletion detected ({delete_count} files removed)"
            )
            severity_score += 2.5

        # Indicator 4: Multi-file breadth
        if unique_files >= cls.HIGH_UNIQUE_FILES_THRESHOLD:
            indicators.append(
                f"Broad filesystem spread ({unique_files} distinct files accessed across {total_ops} ops)"
            )
            severity_score += 1.5

        # Indicator 5: High operational velocity
        if ops_per_sec >= cls.HIGH_OPS_PER_SEC_THRESHOLD:
            indicators.append(
                f"High operational throughput ({ops_per_sec:.2f} operations/second)"
            )
            severity_score += 1.0

        # Combine ML probability and behavioral severity score
        # Scale severity based on ML output
        if rf_prediction == 1:
            severity_score += rf_probability * 4.0
        else:
            severity_score = min(severity_score, 2.5) * (1.0 - rf_probability)

        # Determine qualitative severity level
        if rf_prediction == 0 and severity_score < 2.0:
            severity_level = "NORMAL"
            status_text = "Benign Activity"
        elif severity_score < 4.0:
            severity_level = "LOW RISK"
            status_text = "Minor Activity Elevation"
        elif severity_score < 7.0:
            severity_level = "MEDIUM RISK"
            status_text = "Suspicious Behavioral Burst"
        else:
            severity_level = "HIGH RISK"
            status_text = "Active Ransomware-Like Behavioral Burst"

        # Formulate synthesized reason
        if not indicators:
            if rf_prediction == 1:
                primary_reason = f"Machine learning anomaly detected with {rf_probability*100:.1f}% confidence."
            else:
                primary_reason = "Standard baseline activity within normal operational limits."
        else:
            primary_reason = "; ".join(indicators)

        return {
            "timestamp": timestamp or "N/A",
            "prediction": "Suspicious" if rf_prediction == 1 else "Benign",
            "is_suspicious": bool(rf_prediction == 1),
            "rf_probability": round(float(rf_probability), 4),
            "severity_level": severity_level,
            "severity_score": round(severity_score, 2),
            "status_text": status_text,
            "statusSummary": status_text,
            "primary_reason": primary_reason,
            "indicators": indicators,
            "metrics": {
                "total_ops": total_ops,
                "modify_count": modify_count,
                "rename_count": rename_count,
                "delete_count": delete_count,
                "write_count": write_count,
                "unique_files": unique_files,
                "ops_per_second": ops_per_sec
            }
        }


def explain_scenario_dataframe(
    scenario_df: pd.DataFrame,
    rf_predictions: np.ndarray,
    rf_probabilities: np.ndarray
) -> List[Dict[str, Any]]:
    """
    Generates explainable diagnostic cards for all windows in a scenario DataFrame.
    """
    diagnostics = []
    for idx, (_, row) in enumerate(scenario_df.iterrows()):
        feat_dict = row.to_dict()
        pred = int(rf_predictions[idx])
        prob = float(rf_probabilities[idx])
        ts = str(row.get('window_end', row.get('window_start', 'N/A')))
        diag = ExplainableWarningEngine.evaluate_window(
            features=feat_dict,
            rf_prediction=pred,
            rf_probability=prob,
            timestamp=ts
        )
        diagnostics.append(diag)
    return diagnostics
