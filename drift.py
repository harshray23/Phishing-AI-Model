# drift.py
import joblib
import os
import numpy as np

BASELINE_STATS = None
FEATURES = joblib.load("features.pkl")

if os.path.exists("baseline_stats.pkl"):
    BASELINE_STATS = joblib.load("baseline_stats.pkl")

def detect_drift(X):
    if BASELINE_STATS is None:
        return {
            "status": "disabled",
            "reason": "baseline_stats.pkl not found"
        }

    # Simple PSI-style example
    drift_scores = {}
    for col in X.columns:
        baseline_mean = BASELINE_STATS[col]["mean"]
        current_mean = float(X[col].mean())
        drift_scores[col] = abs(current_mean - baseline_mean)

    return {
        "status": "active",
        "drift_scores": drift_scores
    }
