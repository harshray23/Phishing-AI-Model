# explain.py
import shap
import joblib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
import os

# ---- Load artifacts ----
MODEL = joblib.load("model.pkl")
FEATURES = joblib.load("features.pkl")

# ---- Background dataset (VERY IMPORTANT) ----
# Small zero baseline works well for tree + calibrated models
background = pd.DataFrame(
    np.zeros((1, len(FEATURES))),
    columns=FEATURES
)

masker = shap.maskers.Independent(background)

# ---- Prediction wrapper ----
def predict_fn(X):
    X = pd.DataFrame(X, columns=FEATURES)
    return MODEL.predict_proba(X)[:, 1]

# ---- SHAP explainer (SAFE for calibrated models) ----
explainer = shap.Explainer(
    predict_fn,
    masker=masker,
    feature_names=FEATURES
)

# ---- JSON explanation ----
def explain_prediction(X: pd.DataFrame):
    try:
        shap_values = explainer(X)
        values = shap_values.values[0]
        return dict(zip(FEATURES, np.round(values, 6)))
    except Exception:
        return "SHAP explanation unavailable"

# ---- Waterfall plot ----
def shap_waterfall(X: pd.DataFrame):
    shap_values = explainer(X)

    os.makedirs("plots", exist_ok=True)
    path = f"plots/{uuid.uuid4()}.png"

    plt.figure()
    shap.plots.waterfall(shap_values[0], show=False)
    plt.savefig(path, bbox_inches="tight")
    plt.close()

    return path
