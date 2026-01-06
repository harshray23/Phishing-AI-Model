from fastapi import FastAPI, Query, Request
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
async def predict(url: str = Query(...)):
    features = extract_features(url)

    X = pd.DataFrame([features]).reindex(
        columns=FEATURES,
        fill_value=0
    )

    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0].max()

    return {
        "url": url,
        "prediction": "phishing" if pred == 1 else "legitimate",
        "confidence": round(float(prob), 3)
    }



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
async def drift(url: str = Query(...)):
    features = extract_features(url)

    X = pd.DataFrame([features]).reindex(
        columns=FEATURES,
        fill_value=0
    )

    drift_score = float(X.abs().mean().mean())

    return {
        "url": url,
        "drift_score": round(drift_score, 4),
        "status": "ok"
    }

