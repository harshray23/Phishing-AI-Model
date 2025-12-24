from fastapi import FastAPI
import joblib
import pandas as pd
import traceback

from feature_extractor import extract_features

app = FastAPI(title="Phishing Detection API")

# Load model + features
model = joblib.load("model.pkl")
FEATURES = joblib.load("features.pkl")


@app.get("/")
def root():
    return {"status": "Phishing Detection API running"}


@app.get("/predict")
def predict(url: str):
    try:
        features = extract_features(url)

        # Create DataFrame with correct feature order
        X = pd.DataFrame([features])
        X = X.reindex(columns=FEATURES, fill_value=0)

        # Force numeric (fixes XGBoost object dtype crash)
        X = X.astype(float)

        prob = float(model.predict_proba(X)[0][1])
        prediction = "PHISHING" if prob >= 0.5 else "LEGITIMATE"

        return {
            "url": url,
            "phishing_probability": round(prob, 4),
            "prediction": prediction
        }

    except Exception:
        return {
            "error": "Prediction failed",
            "trace": traceback.format_exc()
        }
