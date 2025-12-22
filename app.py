from fastapi import FastAPI
import joblib
import pandas as pd
from feature_extractor import extract_features

# Initialize FastAPI
app = FastAPI(title="Phishing Detection API")

# Load trained model and feature list
model = joblib.load("model.pkl")
FEATURE_COLUMNS = joblib.load("features.pkl")

@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}

@app.get("/predict")
def predict(url: str):
    # Extract features from URL
    features = extract_features(url)

    # Convert to DataFrame
    X = pd.DataFrame([features])

    # 🔒 Ensure feature alignment with training
    X = X.reindex(columns=FEATURE_COLUMNS, fill_value=0)

    # Predict phishing probability
    prob = float(model.predict_proba(X)[0][1])
    prediction = "PHISHING" if prob >= 0.5 else "LEGITIMATE"

    return {
        "url": url,
        "phishing_probability": round(prob, 4),
        "prediction": prediction
    }
