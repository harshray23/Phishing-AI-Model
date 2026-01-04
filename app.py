from fastapi import FastAPI
import pandas as pd
import joblib

from feature_extractor import extract_features_async
from explain import explain_prediction
from drift import detect_drift

from fastapi.responses import FileResponse
from explain import explain_prediction, shap_waterfall


app = FastAPI()

model = joblib.load("model.pkl")
FEATURES = joblib.load("features.pkl")

@app.get("/predict")
async def predict(url: str, request: Request):
    try:
        features = await extract_features_async(url)
        logger.info(f"Extracted features: {features}")

        X = pd.DataFrame([features]).reindex(columns=FEATURES, fill_value=0)

        prob = float(model.predict_proba(X)[0][1])
        prediction = "PHISHING" if prob > 0.5 else "LEGITIMATE"

        return {
            "url": url,
            "prediction": prediction,
            "probability": round(prob, 4)
        }

    except Exception as e:
        logger.exception("Prediction failed")
        return {"error": str(e)}


@app.post("/batch")
async def batch_predict(urls: list[str]):
    results = []
    for url in urls:
        features = await extract_features_async(url)
        df = pd.DataFrame([features])[FEATURES]
        prob = float(model.predict_proba(df)[0][1])

        results.append({
            "url": url,
            "prediction": "PHISHING" if prob > 0.5 else "LEGIT",
            "confidence": round(prob, 4)
        })
    return results
@app.get("/explain/plot")
async def explain_plot(url: str):
    features = await extract_features_async(url)

    X = pd.DataFrame([features]).reindex(
        columns=FEATURES,
        fill_value=0
    )

    path = shap_waterfall(X)
    return FileResponse(path, media_type="image/png")


@app.get("/explain")
async def explain(url: str):
    features = await extract_features_async(url)

    X = pd.DataFrame([features]).reindex(columns=FEATURES, fill_value=0)

    shap_values = explain_prediction(X)

    return {
        "url": url,
        "shap_values": shap_values
    }
@app.get("/drift")
async def drift(url: str):
    features = await extract_features_async(url)
    X = pd.DataFrame([features]).reindex(columns=FEATURES, fill_value=0)

    drift_scores = detect_drift(X)

    return {
        "url": url,
        "drift_scores": drift_scores,
        "drift_detected": any(v > 3 for v in drift_scores.values())
    }
