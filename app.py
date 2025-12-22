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
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        features = extract_features(url)

        X = pd.DataFrame([features])

        # enforce exact feature order
        X = X.reindex(columns=feature_names, fill_value=0)

        # 🔑 FORCE NUMERIC TYPES (CRITICAL FIX)
        X = X.apply(pd.to_numeric, errors="coerce").fillna(0)

        prob = float(model.predict_proba(X)[0][1])
        prediction = "PHISHING" if prob >= 0.5 else "LEGITIMATE"

        return {
            "url": url,
            "phishing_probability": round(prob, 4),
            "prediction": prediction
        }

    except Exception as e:
        print("❌ Prediction error:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
