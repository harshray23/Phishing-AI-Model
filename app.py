from fastapi import FastAPI
import joblib
import pandas as pd
from feature_extractor import extract_features

app = FastAPI()

# Load model once at startup
model = joblib.load("model.pkl")

@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}

@app.get("/predict")
def predict(url: str):
    features = extract_features(url)
    X = pd.DataFrame([features])

    prob = model.predict_proba(X)[0][1]
    prediction = "PHISHING" if prob >= 0.5 else "LEGITIMATE"

    return {
        "url": url,
        "phishing_probability": round(float(prob), 4),
        "prediction": prediction
    }
