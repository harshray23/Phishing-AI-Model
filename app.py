from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import traceback

from feature_extractor import extract_features

app = FastAPI()

# Load model
model = joblib.load("model.pkl")

# ✅ Get feature names directly from the trained model
feature_names = list(model.feature_names_in_)

@app.get("/")
def root():
    return {"message": "Phishing Detection API is running"}

@app.get("/predict")
def predict(url: str):
    try:
        # Extract features
        features = extract_features(url)

        # Convert to DataFrame
        X = pd.DataFrame([features])

        # ✅ Align features exactly as training
        X = X.reindex(columns=feature_names, fill_value=0)

        # ✅ FORCE numeric types (CRITICAL)
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        # Predict
        prob = float(model.predict_proba(X)[0][1])
        prediction = "PHISHING" if prob >= 0.5 else "LEGITIMATE"

        return {
            "url": url,
            "phishing_probability": round(prob, 4),
            "prediction": prediction
        }

    except Exception as e:
        print("❌ Prediction error:\n", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
