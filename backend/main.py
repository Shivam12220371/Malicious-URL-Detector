from __future__ import annotations

from pathlib import Path

import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from scipy.sparse import hstack

from feature_engineering import extract_struct_features

MODEL_PATH = Path(__file__).with_name("model.pkl")
VECTORIZER_PATH = Path(__file__).with_name("vectorizer.pkl")

app = FastAPI(title="Malicious URL Detector", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://malicious-url-detector-six.vercel.app/"  # Replace with actual URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URLRequest(BaseModel):
    url: str = Field(..., min_length=3, max_length=2048)


class URLResponse(BaseModel):
    prediction: str
    confidence: float
    risk_score: float


@app.on_event("startup")
def load_artifacts() -> None:
    if not MODEL_PATH.exists() or not VECTORIZER_PATH.exists():
        return
    app.state.model = joblib.load(MODEL_PATH)
    app.state.vectorizer = joblib.load(VECTORIZER_PATH)


@app.post("/predict", response_model=URLResponse)
def predict_url(payload: URLRequest) -> URLResponse:
    if not hasattr(app.state, "model"):
        raise HTTPException(
            status_code=500,
            detail="Model not found. Train the model and place model.pkl and vectorizer.pkl in backend/.",
        )

    url = payload.url.strip()
    vectorizer = app.state.vectorizer
    model = app.state.model

    text_features = vectorizer.transform([url])
    struct_features = np.array([extract_struct_features(url)])
    features = hstack([text_features, struct_features])

    proba = model.predict_proba(features)[0][1]
    prediction = "Malicious" if proba >= 0.5 else "Safe"
    risk_score = round(float(proba) * 100, 2)

    return URLResponse(
        prediction=prediction,
        confidence=round(float(max(proba, 1 - proba)) * 100, 2),
        risk_score=risk_score,
    )
